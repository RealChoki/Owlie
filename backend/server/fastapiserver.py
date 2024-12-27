import os
import json
from dotenv import load_dotenv
from fastapi import FastAPI, Request, File, UploadFile, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
from pydantic import BaseModel
from openai import OpenAI
from openai.types.beta.threads.run import RequiredAction, LastError
from tools.fernet import encrypt_data, decrypt_data
from tools.function_calling import get_moodle_course_content
from langchain_experimental.data_anonymizer import PresidioReversibleAnonymizer
from presidio_analyzer import AnalyzerEngine
from presidio_analyzer.nlp_engine import NlpEngineProvider
from langdetect import detect, LangDetectException
import time
import logging
import shutil
import tempfile  # Add this import

# Configure logging
logging.basicConfig(level=logging.ERROR)

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Construct the path to 'config.json' in the same directory as the script
config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.json')

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

# Create configuration containing engine name and models
configuration = {
    "nlp_engine_name": "spacy",
    "models": [{"lang_code": "de", "model_name": "de_core_news_md"},
                {"lang_code": "en", "model_name": "en_core_web_lg"}],
}

# Create NLP engine based on configuration
provider = NlpEngineProvider(nlp_configuration=configuration)
nlp_engine_with_german = provider.create_engine()

# Initialize the analyzer
analyzer = AnalyzerEngine(
    nlp_engine=nlp_engine_with_german, 
    supported_languages=["en", "de"]
)

# Initialize the anonymizer
anonymizer = PresidioReversibleAnonymizer(
    add_default_faker_operators=True,
)

# Detects the language of the text
def detect_language(text: str) -> str:
    try:
        if detect(text) == "en":
            return "en"
        else:
            return "de"
    except LangDetectException:
        return "de"

# A function to check if the message contains PII
def contains_pii(text):
    print("detected language:", detect_language(text))
    results = analyzer.analyze(text=text, language=detect_language(text))
    print("PII results:", results)
    return len(results) > 0

# A function to anonymize the users message
def presidio_anonymize(user_message):
    if contains_pii(user_message):
        print("# # ## # # #  # # ## #  # ## # # # ## # # #  ## # #  # ")
        anonymized_user_message = anonymizer.anonymize(user_message)
        return anonymized_user_message
    return user_message

# A function to de-anonymize the assistants response
def presidio_deanonymize(anonymized_response):
    if contains_pii(anonymized_response):
        print("# # ## # # #  # # ## #  # ## # # # ## # # #  ## # #  # ")
        de_anonymized_response = anonymizer.deanonymize(anonymized_response)
        return de_anonymized_response
    return anonymized_response

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
    if not assistant_id:
        raise ValueError('Assistant IDs not found in configuration.')
    return assistant_id

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

    # Encrypt the assistant_id
    decrypted_assistant_id = decrypt_data(assistant_id)

    thread = client.beta.threads.create()
    encrypted_thread_id = encrypt_data(thread.id)

    client.beta.threads.messages.create(
        thread_id=thread.id,
        content="Greet the user and tell them about yourself and ask what they are looking for.",
        role="user",
        metadata={"type": "hidden"}
    )
    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=decrypted_assistant_id
    )
    return RunStatus(
        run_id=run.id,
        thread_id=encrypted_thread_id,
        status=run.status,
        required_action=run.required_action,
        last_error=run.last_error
    )

@app.get("/api/threads/{thread_id}")
async def get_thread(thread_id: str):
    # Decrypt the thread_id
    decrypted_thread_id = decrypt_data(thread_id)
    
    # Synchronously list messages
    messages = client.beta.threads.messages.list(
        thread_id=decrypted_thread_id
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

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
QUIZ_FILES_DIR = BASE_DIR / 'data' / 'hochschule_fuer_technik_und_wirtschaft_berlin' / 'bachelor' / 'wirtschaftsinformatik' / 'grundlagen_der_programmierung' / 'test'

@app.get("/api/quiz_files")
async def get_quiz_files():
    try:
        # Ensure the directory exists before iterating
        if not QUIZ_FILES_DIR.exists():
            raise FileNotFoundError(f"Quiz files directory not found: {QUIZ_FILES_DIR}")
        
        # Retrieve only .txt filenames as a list of strings
        files = [
            filename.name
            for filename in QUIZ_FILES_DIR.iterdir()
            if filename.is_file() and filename.suffix == ".txt"
        ]

        return files

    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/quiz_files/{filename}")
async def get_quiz_file(filename: str):
    try:
        filepath = QUIZ_FILES_DIR / filename
        if not filepath.exists():
            raise FileNotFoundError(f"Quiz file not found: {filepath}")

        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        return {"title": filename, "content": content}

    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# QUIZ_FILES_DIR = Path('../data/hochschule_fuer_technik_und_wirtschaft_berlin/bachelor/wirtschaftsinformatik/grundlagen_der_programmierung/test')
# @app.get("/api/quiz_files")
# async def get_quiz_files():
#     try:
#         files_data = []
#         # Ensure the directory exists before iterating
#         if not QUIZ_FILES_DIR.exists():
#             raise FileNotFoundError(f"Quiz files directory not found: {QUIZ_FILES_DIR}")

#         for filename in QUIZ_FILES_DIR.iterdir():
#             if filename.is_file() and filename.suffix == ".txt":
#                 filepath = QUIZ_FILES_DIR / filename  # Use path operations
#                 async with open(filepath, "r", encoding="utf-8") as f:
#                     content = await f.read()
#                     files_data.append({"title": filename.name, "content": content})
#         return files_data

#     except FileNotFoundError as e:
#         raise HTTPException(status_code=404, detail=str(e))
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/threads/{thread_id}")
async def post_thread(thread_id: str, message: CreateMessage):
    assistant_id = message.assistant_id
    if not assistant_id:
        return {"error": "Assistant ID is required."}

    # Decrypt the thread_id and assistant_id
    decrypted_thread_id = decrypt_data(thread_id)
    decrypted_assistant_id = decrypt_data(assistant_id)

    # Add user message to the thread
    client.beta.threads.messages.create(
        thread_id=decrypted_thread_id,
        content=message.content,
        role="user"
    )

    # Trigger the assistant to generate a response
    run = client.beta.threads.runs.create(
        thread_id=decrypted_thread_id,
        assistant_id=decrypted_assistant_id
    )

    # Poll for run status updates
    while run.status in ["queued", "processing", "in_progress"]:
        time.sleep(1)  # Wait for 1 second before polling again
        run = client.beta.threads.runs.retrieve(thread_id= decrypted_thread_id, run_id=run.id)

    # Check if the run requires action
    if run.status == "requires_action":
        print("Processing required actions...")
        
        tool_outputs = []

        # Check if there are required actions to submit tool outputs
        if run.required_action and run.required_action.type == "submit_tool_outputs":
            tool_calls = run.required_action.submit_tool_outputs.tool_calls
            # Process each tool call
            for tool_call in tool_calls:
                if tool_call.function.name == "get_moodle_course_content":
                    course_id = "51589"  # Hardcoded for now
                    if course_id:
                        content = get_moodle_course_content(courseid=course_id)

                        # Prepare the tool output with the fetched content
                        print("tool_call.id:", tool_call.id)
                        tool_outputs.append({
                            "tool_call_id": tool_call.id,
                            "output": content
                        })
                    else:
                        print("Course ID is missing in the function arguments.")

            # Submit all tool outputs at once after collecting them in a list
            if tool_outputs:
                print("Submitting tool outputs...")
                try:
                    # Submit tool outputs and poll for the result
                    run = client.beta.threads.runs.submit_tool_outputs_and_poll(
                        thread_id=decrypted_thread_id,
                        run_id=run.id,
                        tool_outputs=tool_outputs
                    )
                    print("Tool outputs submitted successfully.")
                except Exception as e:
                    print(f"Failed to submit tool outputs: {e}")
            else:
                print("No tool outputs to submit.")
        else:
            print("No required actions to process.")

    # Encrypt the thread_id before returning it
    encrypted_thread_id = encrypt_data(decrypted_thread_id)

    # Return the run status
    return RunStatus(
        run_id=run.id,
        thread_id=encrypted_thread_id,
        status=run.status,
        required_action=run.required_action,
        last_error=run.last_error
    )

@app.post("/api/tools/get_moodle_course_content")
async def handle_get_moodle_course_content(request: Request):
    data = await request.json()
    courseid = data.get("courseid")
    if not courseid:
        return {"error": "Course ID is required."}
    try:
        content = get_moodle_course_content(courseid)
        return {"status": "success", "content": content}
    except Exception as e:
        return {"status": "error", "message": str(e)}


@app.get("/api/runs/{thread_id}/{run_id}")
async def get_run_status(thread_id: str, run_id: str):
    try:
        # Fetch run details using both `thread_id` and `run_id`
        decrypted_thread_id = decrypt_data(thread_id)
        run_details = client.beta.threads.runs.retrieve(thread_id=decrypted_thread_id, run_id=run_id)

        return {
            "run_id": run_details.id,
            "thread_id": run_details.thread_id,
            "status": run_details.status,
            "required_action": run_details.required_action,
            "last_error": run_details.last_error
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/threads/{thread_id}/send_and_wait")
async def send_message_and_wait_for_response(thread_id: str, message: CreateMessage):
    assistant_id = message.assistant_id
    if not assistant_id:
        return {"error": "Assistant ID is required."}

    # Decrypt the thread_id and assistant_id
    decrypted_thread_id = decrypt_data(thread_id)
    decrypted_assistant_id = decrypt_data(assistant_id)

    # Check thread state
    while True:
        try:
            # Check for active runs on the thread
            active_runs = client.beta.threads.runs.list(thread_id=decrypted_thread_id)
            if active_runs.data and any(run.status in ["queued", "processing", "in_progress"] for run in active_runs.data):
                print("Thread is active; waiting for it to become available.")
                time.sleep(1)  # Wait before retrying
            else:
                print("Thread is now available.")
                break
        except Exception as e:
            print(f"Error checking for active runs: {e}")
            return {"error": f"Failed to check for active runs: {e}"}

    try:
        print("Unencrypted user message:", message.content)
        anonymized_message = presidio_anonymize(message.content)
        print("Anonymized user message:", anonymized_message)
        client.beta.threads.messages.create(
            thread_id=decrypted_thread_id,
            content=anonymized_message,
            role="user"
        )
    except Exception as e:
        return {"error": f"Failed to send message: {e}"}

    try:
        run = client.beta.threads.runs.create(
            thread_id=decrypted_thread_id,
            assistant_id=decrypted_assistant_id
        )
    except Exception as e:
        return {"error": f"Failed to start conversation run: {e}"}


    # Step 1: Poll for run status updates
    while run.status in ["queued", "processing", "in_progress"]:
        time.sleep(1)  # Wait for 1 second before polling again
        run = client.beta.threads.runs.retrieve(thread_id=decrypted_thread_id, run_id=run.id)

    # Step 2: Handle actions if required
    if run.status == "requires_action":
        print("Processing required actions...")
        tool_outputs = []

        if run.required_action and run.required_action.type == "submit_tool_outputs":
            tool_calls = run.required_action.submit_tool_outputs.tool_calls
            for tool_call in tool_calls:
                if tool_call.function.name == "get_moodle_course_content":
                    course_id = "51589"  # Hardcoded for now
                    if course_id:
                        content = get_moodle_course_content(courseid=course_id)

                        # Prepare the tool output with the fetched content
                        print("tool_call.id:", tool_call.id)
                        tool_outputs.append({
                            "tool_call_id": tool_call.id,
                            "output": content
                        })
                    else:
                        print("Course ID is missing in the function arguments.")

            if tool_outputs:
                print("Submitting tool outputs...")
                try:
                    run = client.beta.threads.runs.submit_tool_outputs_and_poll(
                        thread_id=decrypted_thread_id,
                        run_id=run.id,
                        tool_outputs=tool_outputs
                    )
                    print("Tool outputs submitted successfully.")
                except Exception as e:
                    print(f"Failed to submit tool outputs: {e}")
            else:
                print("No tool outputs to submit.")
        else:
            print("No required actions to process.")

    # Step 3: Fetch the latest assistant messages
    messages = client.beta.threads.messages.list(thread_id=decrypted_thread_id)

    if messages.data:
        for latest_message in messages.data:
            if latest_message.role == "assistant":
                content = "Ein Fehler ist aufgetreten. Bitte versuchen Sie es erneut."
                
                if hasattr(latest_message, 'content') and latest_message.content:
                    if isinstance(latest_message.content, list) and latest_message.content:
                        content_block = latest_message.content[0]
                        if hasattr(content_block, 'text') and hasattr(content_block.text, 'value'):
                            content = content_block.text.value
                            print("anonynmized ai response:", content)
                            deanonymized_response = presidio_deanonymize(content)
                            print("deanonymized ai response:", deanonymized_response)

                return ThreadMessage(
                    content=deanonymized_response,
                    role=latest_message.role,
                    hidden="type" in latest_message.metadata and latest_message.metadata.get("type") == "hidden",
                    id=latest_message.id,
                    created_at=latest_message.created_at
                )

    return {"error": "No assistant response found."}

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
        assistant_id = get_assistant_ids(course_name, mode_name)
        
        # Encrypt the assistant_id and before returning them
        encrypted_assistant_id = encrypt_data(assistant_id)
        
        return {"assistant_id": encrypted_assistant_id,}
    except ValueError as e:
        return {"error": str(e)}

@app.post("/api/upload")
async def upload_files(
    thread_id: str = Form(...),
    files: List[UploadFile] = File(...),
    current_course: str = Form(...),
    current_mode: str = Form(...),
    assistant_id: Optional[str] = Form(None)  # Optional parameter
):
    global assistant_cache  # Use assistant_cache to store assistants per thread

    if not files:
        return {"error": "No files uploaded"}
        
    mode_config = get_course_config(current_course, current_mode)
    vector_store_id = mode_config.get('vector_store_id')

    # Decrypt the thread_id, vector_store_id, and assistant_id if provided
    decrypted_thread_id = decrypt_data(thread_id)
    decrypted_assistant_id = decrypt_data(assistant_id) if assistant_id else None

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

    # Retrieve file IDs from the default vector store
    default_files = client.beta.vector_stores.files.list(vector_store_id)
    default_file_ids = [file.id for file in default_files.data]

    # Combine file IDs
    combined_file_ids = default_file_ids + file_ids

    # Create a new vector store with combined files
    vector_store = client.beta.vector_stores.create(
        name=f"Temporary Vector Store for Thread {decrypted_thread_id}",
        file_ids=combined_file_ids
    )
    temporary_vector_store_id = vector_store.id
    print(f"Created temporary vector store: {temporary_vector_store_id}")

    if decrypted_assistant_id:
        # Update the existing assistant with the new vector store files
        client.beta.assistants.update(
            assistant_id=decrypted_assistant_id,
            tool_resources={
                "file_search": {
                    "vector_store_ids": [temporary_vector_store_id]
                }
            }
        )
        print(f"Updated assistant: {decrypted_assistant_id}")
        temporary_assistant_id = decrypted_assistant_id
    else:
        # Retrieve assistant configuration from config.json
        mode_config = get_course_config(current_course, current_mode)
        instructions = mode_config['instructions']
        tools = mode_config['tools']
        model = mode_config['model']

        # Update tool resources to include the new vector store ID
        tool_resources = {
            "file_search": {
                "vector_store_ids": [temporary_vector_store_id]
            }
        }
        
        # Create a new temporary assistant using the configuration
        temporary_assistant = client.beta.assistants.create(
            instructions=instructions,
            name=f"Temporary Assistant for Thread {decrypted_thread_id}",
            tools=tools,
            tool_resources=tool_resources,
            model=model
        )
        temporary_assistant_id = temporary_assistant.id
        print(f"Created temporary assistant: {temporary_assistant_id}")

    # Associate the temporary assistant with the thread
    assistant_cache[decrypted_thread_id] = {
        "assistant_id": temporary_assistant_id,
        "vector_store_id": temporary_vector_store_id
    }

    # Encrypt the thread_id, assistant_id, and vector_store_id before returning them
    encrypted_thread_id = encrypt_data(decrypted_thread_id)
    encrypted_assistant_id = encrypt_data(temporary_assistant_id)
    encrypted_vector_store_id = encrypt_data(temporary_vector_store_id)

    return {
        "message": "Temporary assistant created and files uploaded successfully",
        "temporary_assistant_id": encrypted_assistant_id,
        "thread_id": encrypted_thread_id,
        "vector_store_id": encrypted_vector_store_id
    }

@app.post("/api/delete_temp_assistant")
async def delete_temp_assistant(request: Request):
    data = await request.json()
    old_thread_id = decrypt_data(data.get('old_thread_id'))

    if not old_thread_id:
        return {"error": "Old thread ID is required."}

    # Check if there's a temporary assistant associated with this thread
    assistant_info = assistant_cache.get(old_thread_id)
    if assistant_info:
        # Delete the temporary assistant
        try:
            client.beta.assistants.delete(assistant_info['assistant_id'])
            print(f"Deleted temporary assistant: {assistant_info['assistant_id']}")
        except Exception as e:
            print(f"Error deleting assistant: {e}")

        # Delete the temporary vector store
        try:
            client.beta.vector_stores.delete(assistant_info['vector_store_id'])
            print(f"Deleted temporary vector store: {assistant_info['vector_store_id']}")
        except Exception as e:
            print(f"Error deleting vector store: {e}")

        # Remove from cache
        del assistant_cache[old_thread_id]

    return {"message": f"Switched from thread {old_thread_id}"}


# validating	the input file is being validated before the batch can begin
# failed	the input file has failed the validation process
# in_progress	the input file was successfully validated and the batch is currently being run
# finalizing	the batch has completed and the results are being prepared
# completed	the batch has been completed and the results are ready
# expired	the batch was not able to be completed within the 24-hour time window
# cancelling	the batch is being cancelled (may take up to 10 minutes)
# cancelled	the batch was cancelled