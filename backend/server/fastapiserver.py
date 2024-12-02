import os
import json
from dotenv import load_dotenv
from fastapi import FastAPI, Request, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
from pydantic import BaseModel
from openai import OpenAI, AssistantEventHandler
from openai.types.beta.threads.run import RequiredAction, LastError
from openai.types.beta.threads.run_submit_tool_outputs_params import ToolOutput
from function_calling import get_moodle_course_content
import logging
import shutil
import tempfile  # Add this import

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Get the directory of the current script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Construct the path to 'config.json' one level up
config_path = os.path.join(BASE_DIR, '..', 'config.json')

# Load and parse config.json
with open(config_path, 'r') as f:
    config_data = json.load(f)

# Initialize FastAPI application
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variables for assistant and vector store IDs
assistant_id = None
vector_store_id = None
current_course = None
current_mode = None
assistant_cache = {}  # Cache assistants for reuse
FILES_DIR = ""
file_ids = []

# Configure logging
logging.basicConfig(level=logging.ERROR)

def get_course_config(course_name, mode_name):
    # Traverse the config to find the matching course and mode
    for university in config_data['universities'].values():
        for degree_level in university.values():
            for subject in degree_level.values():
                course = subject.get(course_name)
                if course and mode_name in course:
                    return course[mode_name]
    raise ValueError('Course or mode not found in config')

def get_course_id(config, university, degree, subject, course):
    return config['universities'][university][degree][subject][course]['course_id']

def initialize_assistant(course_name, mode_name):
    global assistant_id, vector_store_id, FILES_DIR, file_ids, current_course, current_mode

    try:
        assistant_key = f"{course_name}_{mode_name}"
        if assistant_key in assistant_cache:
            assistant_id = assistant_cache[assistant_key]['assistant_id']
            vector_store_id = assistant_cache[assistant_key]['vector_store_id']
            current_course = course_name
            current_mode = mode_name
            return assistant_id, vector_store_id

        mode_config = get_course_config(course_name, mode_name)

        instructions = mode_config['instructions']
        data_path = mode_config['data_path']
        tools = mode_config['tools']
        model = mode_config['model']

        FILES_DIR = os.path.abspath(os.path.join(BASE_DIR, '..', data_path))
        if not os.path.exists(FILES_DIR):
            raise FileNotFoundError(f"Data path {FILES_DIR} does not exist.")

        file_ids = []

        # Upload files to OpenAI
        for file in sorted(os.listdir(FILES_DIR)):
            file_path = os.path.join(FILES_DIR, file)
            if os.path.isfile(file_path):
                with open(file_path, "rb") as f:
                    _file = client.files.create(file=f, purpose="assistants")
                    file_ids.append(_file.id)
                    print(f"Uploaded file: {_file.id} - {file}")
            else:
                print(f"Skipping {file_path}, not a file.")

        if not file_ids:
            raise ValueError("No files were uploaded. Please check the data directory.")

        # **Add the vector store creation here**
        if vector_store_id is None:
            # Create an initial vector store if one doesn't exist
            vector_store = client.beta.vector_stores.create(
                name=f"{course_name} - {mode_name}",
                file_ids=file_ids
            )
            vector_store_id = vector_store.id
            print(f"Created vector store: {vector_store_id} - {vector_store.name}")

        # Create assistant with the updated vector store
        assistant = client.beta.assistants.create(
            instructions=instructions,
            name=f"{course_name} - {mode_name} Assistant",
            tools=tools,
            tool_resources={"file_search": {"vector_store_ids": [vector_store_id]}},
            model=model,
        )
        assistant_id = assistant.id
        current_course = course_name
        current_mode = mode_name

        # Cache the assistant for future use
        assistant_cache[assistant_key] = {
            'assistant_id': assistant_id,
            'vector_store_id': vector_store_id
        }
        return assistant_id, vector_store_id
    except Exception as e:
        logging.error(f"Error initializing assistant: {e}")
        raise e  # Re-raise exception to trigger a 500 response

# Add an endpoint to set the assistant based on course and mode
@app.post("/api/set_assistant")
async def set_assistant(request: Request):
    data = await request.json()
    course_name = data.get('course_name')
    mode_name = data.get('mode_name')

    if not course_name or not mode_name:
        return {"error": "Course name and mode name are required"}

    try:
        assistant_id, vector_store_id = initialize_assistant(course_name, mode_name)
        return {"message": "Assistant updated successfully", "assistant_id": assistant_id, "vector_store_id": vector_store_id}
    except ValueError as e:
        return {"error": str(e)}

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
                    course_id = arguments.get("courseid", get_course_id(config_data, 'hochschule_fuer_technik_und_wirtschaft_berlin', 'bachelor', 'wirtschaftsinformatik', 'grundlagen_der_programmierung'))
                    result = get_moodle_course_content(course_id)
                    tool_outputs.append({"tool_call_id": tool.id, "output": result})
                except (json.JSONDecodeError, ValueError) as e:
                    print(f"Error processing course content: {e}")
                    tool_outputs.append({"tool_call_id": tool.id, "output": "Error fetching course content"})
            elif tool.function.name == "file_search":
                try:
                    arguments = json.loads(tool.function.arguments)
                    query = arguments.get("query", "")
                    search_results = perform_file_search(query, vector_store_id)
                    tool_outputs.append({"tool_call_id": tool.id, "output": search_results})
                except (json.JSONDecodeError, ValueError) as e:
                    print(f"Error processing file search: {e}")
                    tool_outputs.append({"tool_call_id": tool.id, "output": "Error performing file search"})
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

def perform_file_search(query: str, vector_store_id: str):
    try:
        search_response = client.beta.vector_stores.query(
            vector_store_id=vector_store_id,
            query=query,
            top_k=5  # Number of results to return
        )
        results = [doc['content'] for doc in search_response.data]
        return results
    except Exception as e:
        logging.error(f"Error performing file search: {e}")
        return ["Error performing file search"]

# Update endpoints to check if assistant_id is initialized
@app.post("/api/new")
def post_new():
    if assistant_id is None:
        return {"error": "Assistant is not initialized. Please set the assistant using /api/set_assistant."}
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
    if assistant_id is None:
        return {"error": "Assistant is not initialized. Please set the assistant using /api/set_assistant."}
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

@app.get("/api/threads/{thread_id}/latest_message")
async def get_latest_message(thread_id: str):
    # Fetch the last message only
    messages = client.beta.threads.messages.list(
        thread_id=thread_id
    )
    
    if not messages.data:
        return {"message": "No messages in the thread."}

    latest_message = messages.data[0]  # Get the latest message
    return ThreadMessage(
        content=latest_message.content[0].text.value,
        role=latest_message.role,
        hidden="type" in latest_message.metadata and latest_message.metadata["type"] == "hidden",
        id=latest_message.id,
        created_at=latest_message.created_at
    )

import asyncio

@app.post("/api/threads/{thread_id}/run_and_get_latest")
async def run_and_get_latest(thread_id: str, message: CreateMessage):
    if assistant_id is None:
        return {"error": "Assistant is not initialized. Please set the assistant using /api/set_assistant."}
    # Post the message to the thread
    client.beta.threads.messages.create(
        thread_id=thread_id,
        content=message.content,
        role="user"
    )

    # Create a run for the assistant
    run = client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=assistant_id
    )

    # Wait for the assistant to process the message
    await asyncio.sleep(0.1)  # Adjust the delay as needed

    # Fetch the latest message until it is different from the user's message
    latest_message = None
    for _ in range(10):  # Retry up to 10 times
        messages = client.beta.threads.messages.list(
            thread_id=thread_id
        )
        
        if messages.data and messages.data[0].role != "user":
            latest_message = messages.data[0]
            break
        
        await asyncio.sleep(1)  # Wait before retrying

    if not latest_message:
        return {"message": "No response from the assistant."}

    return {
        "run_status": RunStatus(
            run_id=run.id,
            thread_id=thread_id,
            status=run.status,
            required_action=run.required_action,
            last_error=run.last_error
        ),
        "latest_message": ThreadMessage(
            content=latest_message.content[0].text.value,
            role=latest_message.role,
            hidden="type" in latest_message.metadata and latest_message.metadata["type"] == "hidden",
            id=latest_message.id,
            created_at=latest_message.created_at
        )
    }


@app.post("/api/threads/{thread_id}/send_and_wait")
async def send_message_and_wait_for_response(thread_id: str, message: CreateMessage):
    if assistant_id is None:
        return {"error": "Assistant is not initialized. Please set the assistant using /api/set_assistant."}
    # Step 1: Post the message to the assistant
    client.beta.threads.messages.create(
        thread_id=thread_id,
        content=message.content,
        role="user"
    )

    # Start the conversation run
    client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=assistant_id
    )

    # Step 2: Wait for the assistant's response indefinitely
    wait_interval = 5

    while True:
        await asyncio.sleep(wait_interval)

        # Fetch the latest messages
        messages = client.beta.threads.messages.list(
            thread_id=thread_id
        )
        
        if messages.data:
            # Look for the first assistant response
            for latest_message in messages.data:
                if latest_message.role == "assistant":
                    # Attempt to extract the content safely
                    content = "Ein Fehler ist aufgetreten. Bitte versuchen Sie es erneut."
                    
                    # Directly access content attributes if it's a TextContentBlock object
                    if hasattr(latest_message, 'content') and latest_message.content:
                        if isinstance(latest_message.content, list) and latest_message.content:
                            # Access the first content block
                            content_block = latest_message.content[0]
                            if hasattr(content_block, 'text') and hasattr(content_block.text, 'value'):
                                content = content_block.text.value
                        
                    return ThreadMessage(
                        content=content,
                        role=latest_message.role,
                        hidden="type" in latest_message.metadata and latest_message.metadata.get("type") == "hidden",
                        id=latest_message.id,
                        created_at=latest_message.created_at
                    )

@app.post("/api/upload")
async def upload_files(files: List[UploadFile] = File(...)):
    global vector_store_id, assistant_id

    if not files:
        return {"error": "No files uploaded"}

    file_ids = []

    for uploaded_file in files:
        # Get the system's temporary directory
        temp_dir = tempfile.gettempdir()
        temp_file_path = os.path.join(temp_dir, uploaded_file.filename)
        
        # Save the file temporarily
        with open(temp_file_path, "wb") as buffer:
            shutil.copyfileobj(uploaded_file.file, buffer)

        # Upload the file to OpenAI
        with open(temp_file_path, "rb") as f:
            _file = client.files.create(file=f, purpose="assistants")
            file_ids.append(_file.id)
            print(f"Uploaded file: {_file.id} - {uploaded_file.filename}")

        # Optionally delete the temp file after upload
        os.remove(temp_file_path)

    # Update the vector store with new files
    if vector_store_id is None:
        # Create a new vector store if it doesn't exist
        vector_store = client.beta.vector_stores.create(
            name="User Uploaded Files",
            file_ids=file_ids
        )
        vector_store_id = vector_store.id
        print(f"Created vector store: {vector_store_id}")
    else:
        # Retrieve existing file IDs from the vector store
        existing_files = client.beta.vector_stores.files.list(vector_store_id=vector_store_id)
        existing_file_ids = [file.id for file in existing_files.data]
        updated_file_ids = existing_file_ids + file_ids

        # Add new files to the vector store
        for file_id in updated_file_ids:
            client.beta.vector_stores.files.create(
                vector_store_id=vector_store_id,
                file_id=file_id
            )
            print(f"Added file {file_id} to vector store: {vector_store_id}")

    # Update the assistant's tool resources to include the updated vector store
    client.beta.assistants.update(
        assistant_id=assistant_id,
        tool_resources={"file_search": {"vector_store_ids": [vector_store_id]}}
    )

    return {"message": "Files uploaded and vector store updated successfully"}

# validating	the input file is being validated before the batch can begin
# failed	the input file has failed the validation process
# in_progress	the input file was successfully validated and the batch is currently being run
# finalizing	the batch has completed and the results are being prepared
# completed	the batch has been completed and the results are ready
# expired	the batch was not able to be completed within the 24-hour time window
# cancelling	the batch is being cancelled (may take up to 10 minutes)
# cancelled	the batch was cancelled