import os
import json
from dotenv import load_dotenv
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
from pydantic import BaseModel
from openai import OpenAI, AssistantEventHandler
from openai.types.beta.threads.run import RequiredAction, LastError
from openai.types.beta.threads.run_submit_tool_outputs_params import ToolOutput
from function_calling import get_moodle_course_content

# Load environment variables
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Initialize FastAPI application
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variables for assistant and vector store IDs
assistant_id = None
vector_store_id = None
FILES_DIR = "../data/"
file_ids = []

# Helper data models
class RunStatus(BaseModel):
    run_id: str
    thread_id: str
    status: str
    required_action: Optional[RequiredAction]
    last_error: Optional[LastError]


class ThreadMessage(BaseModel):
    content: str
    role: str
    hidden: bool
    id: str
    created_at: int


class Thread(BaseModel):
    messages: List[ThreadMessage]


class CreateMessage(BaseModel):
    content: str

# Event handler class for managing assistant actions
class EventHandler(AssistantEventHandler):

    def on_event(self, event):
        if event.event == 'thread.run.requires_action':
            run_id = event.data.id
            self.handle_requires_action(event.data, run_id)

    def on_text_created(self, text) -> None:
        if hasattr(text, 'value'):
            print(f"\nAssistant: {text.value}", end="", flush=True)
        else:
            print(f"\nAssistant: {text}", end="", flush=True)

    def on_text_delta(self, delta, snapshot):
        print(f"Text Delta: {delta.value}", end="", flush=True)

    def handle_requires_action(self, data, run_id):
        tool_outputs = []
        for tool in data.required_action.submit_tool_outputs.tool_calls:
            if tool.function.name == "get_moodle_course_content":
                try:
                    arguments = json.loads(tool.function.arguments)
                    course_id = arguments.get("courseid", "51589")
                    result = get_moodle_course_content(course_id)
                    tool_outputs.append({"tool_call_id": tool.id, "output": result})
                except (json.JSONDecodeError, ValueError) as e:
                    print(f"Error processing course content: {e}")
                    tool_outputs.append({"tool_call_id": tool.id, "output": "Error fetching course content"})
        self.submit_tool_outputs(tool_outputs, run_id)

    def submit_tool_outputs(self, tool_outputs, run_id):
        with client.beta.threads.runs.submit_tool_outputs_stream(
            thread_id=self.current_run.thread_id,
            run_id=self.current_run.id,
            tool_outputs=tool_outputs,
            event_handler=self  # Ensure the current handler is used
        ) as stream:
            for text in stream.text_deltas:
                print(f"Received Text Delta: {text.value}", end="", flush=True)
            print("Stream finished")

# Function to initialize the assistant and upload resources
def initialize_assistant():
    global assistant_id, vector_store_id

    # Upload files to OpenAI
    for file in sorted(os.listdir(FILES_DIR)):
        with open(os.path.join(FILES_DIR, file), "rb") as f:
            _file = client.files.create(file=f, purpose="assistants")
            file_ids.append(_file.id)
            print(f"Uploaded file: {_file.id} - {file}")

    # Create a vector store for course content
    vector_store = client.beta.vector_stores.create(
        name="Vorlesungsuntertitel zu den Grundlagen der Programmierung",
        file_ids=file_ids
    )
    vector_store_id = vector_store.id
    print(f"Created vector store: {vector_store_id} - {vector_store.name}")


    # Instructions for test programming assistant
    # instructions = (
    #     " Du bist ein interaktiver Mentor für Programmierkonzepte. Stelle eine Frage nach der anderen in vorgegebener"
    #     " Reihenfolge. Bei Schwierigkeiten stelle gezielte Fragen oder gib Erklärungen und Beispiele. Wiederhole Themen,"
    #     " bei denen der Benutzer unsicher ist, und überprüfe das Verständnis mit Kontrollfragen. Gratuliere bei Erfolg"
    #     " und gib Aufgaben zu schwierigen Themen. Dokumentiere behandelte und offene Themen klar."
    # )

    # Instructions for general programming assistant
    instructions = (
        " Du bist ein freundlicher und unterstützender Lehrassistent für das Modul Grundlagen der Programmierung"
        " Deine Aufgabe ist es Erstsemester-Studierende zur Lösung zu führen ohne jedoch vollständige Lösungen zu"
        " geben Bespreche keine Themen die nicht in den Vorlesungsskripten behandelt werden wie zum Beispiel Listen"
        " Deine Unterstützung soll das Verständnis fördern und das selbstständige Denken anregen ohne die akademische"
        " Integrität zu gefährden Verwende bei Bedarf Pseudocode im folgenden Format"
        " START"
        "     INITIALISIERE sum mit 0"
        "     FÜR jede Zahl von 1 bis 5 MACH"
        "         ADDIERE die Zahl zu sum"
        "     ENDE FÜR"
        "     GIB sum aus"
        " END"
    )

    # Register the assistant and add the Moodle function as a callable tool
    assistant = client.beta.assistants.create(
        instructions=instructions,
        name="HTWCodingMentor",
        tools=[{
            "type": "function",
            "function": {
                "name": "get_moodle_course_content",
                "description": "Fetches Moodle course content based on course ID.",
                "parameters": {
                    "type": "object",
                    "required": ["courseid"],
                    "properties": {
                        "courseid": {
                            "type": "string",
                            "description": "The Moodle course ID, e.g., '51589'."
                        }
                    },
                    "additionalProperties": False
                }
            }
        }],
        tool_resources={"file_search": {"vector_store_ids": [vector_store_id]}},
        model="gpt-4o-mini",
    )
    assistant_id = assistant.id
    print(f"Created assistant: {assistant_id} - {assistant.name}")

# Initialize the assistant when the server starts
initialize_assistant()

# API Endpoints

@app.post("/api/new")
def post_new():
    thread = client.beta.threads.create()
    client.beta.threads.messages.create(
        thread_id=thread.id,
        content="Greet the user and tell them about yourself and ask what they are looking for.",
        role="user",
        metadata={"type": "hidden"}
    )
    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant_id
    )
    return RunStatus(
        run_id=run.id,
        thread_id=thread.id,
        status=run.status,
        required_action=run.required_action,
        last_error=run.last_error
    )


@app.get("/api/threads/{thread_id}/runs/{run_id}")
async def get_run(thread_id: str, run_id: str):
    run = client.beta.threads.runs.retrieve(
        thread_id=thread_id,
        run_id=run_id
    )

    return RunStatus(
        run_id=run.id,
        thread_id=thread_id,
        status=run.status,
        required_action=run.required_action,
        last_error=run.last_error
    )


@app.post("/api/threads/{thread_id}/runs/{run_id}/tool")
def post_tool(thread_id: str, run_id: str, tool_outputs: List[ToolOutput]):
    run = client.beta.threads.runs.submit_tool_outputs(
        run_id=run_id,
        thread_id=thread_id,
        tool_outputs=tool_outputs
    )
    return RunStatus(
        run_id=run.id,
        thread_id=thread_id,
        status=run.status,
        required_action=run.required_action,
        last_error=run.last_error
    )


@app.get("/api/threads/{thread_id}")
async def get_thread(thread_id: str):
    # Synchronously list messages
    messages = client.beta.threads.messages.list(
        thread_id=thread_id
    )

    result = [
        ThreadMessage(
            content=message.content[0].text.value,
            role=message.role,
            hidden="type" in message.metadata and message.metadata["type"] == "hidden",
            id=message.id,
            created_at=message.created_at
        )
        for message in messages.data
    ]

    return Thread(
        messages=result,
    )

@app.post("/api/threads/{thread_id}")
async def post_thread(thread_id: str, message: CreateMessage):
    client.beta.threads.messages.create(
        thread_id=thread_id,
        content=message.content,
        role="user"
    )

    run = client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=assistant_id
    )

    return RunStatus(
        run_id=run.id,
        thread_id=thread_id,
        status=run.status,
        required_action=run.required_action,
        last_error=run.last_error
    )

@app.websocket("/ws/{thread_id}/{run_id}")
async def websocket_endpoint(websocket: WebSocket, thread_id: str, run_id: str):
    await websocket.accept()

    stream = client.beta.threads.runs.submit_tool_outputs_stream(
        thread_id=thread_id, 
        run_id=run_id,
        tool_outputs=[]
    )

    try:
        for message in stream:
            await websocket.send_text(message.value)
    except Exception as e:
        await websocket.send_text(f"Error: {str(e)}")
    finally:
        await websocket.close()

@app.get("/api/threads/{thread_id}/latest_message")
async def get_latest_message(thread_id: str):
    # Fetch the last message only
    messages = client.beta.threads.messages.list(
        thread_id=thread_id
    )
    
    if not messages.data:
        return {"message": "No messages in the thread."}

    latest_message = messages.data[-1]  # Get the latest message
    return ThreadMessage(
        content=latest_message.content[0].text.value,
        role=latest_message.role,
        hidden="type" in latest_message.metadata and latest_message.metadata["type"] == "hidden",
        id=latest_message.id,
        created_at=latest_message.created_at
    )
