import os
import json
import asyncio
from dotenv import load_dotenv
from fastapi import FastAPI, Request, File, UploadFile, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
from pydantic import BaseModel
from openai import OpenAI, AssistantEventHandler
from openai.types.beta.threads.run import RequiredAction, LastError
from openai.types.beta.threads.run_submit_tool_outputs_params import ToolOutput
from tools.function_calling import get_moodle_course_content
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

def get_assistant_ids(course_name, mode_name):
    mode_config = get_course_config(course_name, mode_name)
    assistant_id = mode_config.get('assistant_id')
    vector_store_id = mode_config.get('vector_store_id')
    if not assistant_id or not vector_store_id:
        raise ValueError('Assistant IDs not found in configuration.')
    return assistant_id, vector_store_id



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
    assistant_id: Optional[str]


# Update endpoints to check if assistant_id is initialized
@app.post("/api/new")
async def post_new(request: Request):
    data = await request.json()
    assistant_id = data.get('assistant_id')

    if not assistant_id:
        return {"error": "Assistant ID is required."}

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

@app.post("/api/threads/{thread_id}/send_and_wait")
async def send_message_and_wait_for_response(thread_id: str, message: CreateMessage):
    assistant_id = message.assistant_id
    if not assistant_id:
        return {"error": "Assistant ID is required."}

    # Post the message to the thread
    client.beta.threads.messages.create(
        thread_id=thread_id,
        content=message.content,
        role="user"
    )

    # Start the conversation run with the provided assistant_id
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

@app.get("/api/courses")
async def get_courses(university: str, degree: str, subject: str):
    try:
        university_data = config_data['universities'].get(university)
        if not university_data:
            raise KeyError(f"University '{university}' not found.")

        degree_data = university_data.get(degree)
        if not degree_data:
            raise KeyError(f"Degree '{degree}' not found.")

        subject_data = degree_data.get(subject)
        if not subject_data:
            raise KeyError(f"Subject '{subject}' not found.")

        course_names = list(subject_data.keys())
        return {"courses": course_names}
    
    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.get("/api/get_assistant_ids")
async def get_assistant_ids_endpoint(course_name: str, mode_name: str):
    try:
        assistant_id, vector_store_id = get_assistant_ids(course_name, mode_name)
        return {"assistant_id": assistant_id, "vector_store_id": vector_store_id}
    except ValueError as e:
        return {"error": str(e)}

@app.post("/api/upload")
async def upload_files(
    thread_id: str = Form(...),
    vector_store_id: str = Form(...),
    files: List[UploadFile] = File(...)
):
    print(f"Thread ID: {thread_id}")
    print(f"Vector Store ID: {vector_store_id}")
    for uploaded_file in files:
        print(f"Filename: {uploaded_file.filename}")
    return {"message": "Files received successfully"}

# validating	the input file is being validated before the batch can begin
# failed	the input file has failed the validation process
# in_progress	the input file was successfully validated and the batch is currently being run
# finalizing	the batch has completed and the results are being prepared
# completed	the batch has been completed and the results are ready
# expired	the batch was not able to be completed within the 24-hour time window
# cancelling	the batch is being cancelled (may take up to 10 minutes)
# cancelled	the batch was cancelled