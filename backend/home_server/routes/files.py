from tools.fernet import decrypt_data
from pathlib import Path
import os
import shutil
import tempfile
from typing import List, Optional
from fastapi import APIRouter, File, Form, Request, UploadFile
from tools.fernet import decrypt_data, encrypt_data
from tools.config_loader import get_course_config  # Move get_course_config here
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Router for file management
router = APIRouter()

# Assistant cache for tracking temporary assistants
assistant_cache = {}

@router.post("/upload")
async def upload_files(
    thread_id: str = Form(...),
    files: List[UploadFile] = File(...),
    current_course: str = Form(...),
    current_mode: str = Form(...),
    assistant_id: Optional[str] = Form(None)  
):
    if not files:
        return {"error": "No files uploaded"}

    mode_config = get_course_config(current_course, current_mode)
    vector_store_id = mode_config.get('vector_store_id')

    decrypted_thread_id = decrypt_data(thread_id)
    decrypted_assistant_id = decrypt_data(assistant_id) if assistant_id else None

    file_ids = []
    for uploaded_file in files:
        temp_dir = tempfile.gettempdir()
        temp_file_path = Path(temp_dir) / uploaded_file.filename

        with open(temp_file_path, "wb") as buffer:
            shutil.copyfileobj(uploaded_file.file, buffer)

        with open(temp_file_path, "rb") as f:
            _file = client.files.create(file=f, purpose="assistants")
            file_ids.append(_file.id)

        os.remove(temp_file_path)

    default_files = client.beta.vector_stores.files.list(vector_store_id)
    default_file_ids = [file.id for file in default_files.data]
    combined_file_ids = default_file_ids + file_ids

    vector_store = client.beta.vector_stores.create(
        name=f"Temporary Vector Store for Thread {decrypted_thread_id}",
        file_ids=combined_file_ids
    )
    temporary_vector_store_id = vector_store.id

    if decrypted_assistant_id:
        client.beta.assistants.update(
            assistant_id=decrypted_assistant_id,
            tool_resources={"file_search": {"vector_store_ids": [temporary_vector_store_id]}}
        )
        temporary_assistant_id = decrypted_assistant_id
    else:
        instructions = mode_config['instructions']
        tools = mode_config['tools']
        model = mode_config['model']
        
        temporary_assistant = client.beta.assistants.create(
            instructions=instructions,
            name=f"Temporary Assistant for Thread {decrypted_thread_id}",
            tools=tools,
            tool_resources={"file_search": {"vector_store_ids": [temporary_vector_store_id]}},
            model=model
        )
        temporary_assistant_id = temporary_assistant.id

    assistant_cache[decrypted_thread_id] = {
        "assistant_id": temporary_assistant_id,
        "vector_store_id": temporary_vector_store_id,
        "file_ids": file_ids
    }

    return {
        "message": "Temporary assistant created and files uploaded successfully",
        "temporary_assistant_id": encrypt_data(temporary_assistant_id),
        "thread_id": encrypt_data(decrypted_thread_id),
        "vector_store_id": encrypt_data(temporary_vector_store_id)
    }

@router.post("/delete_temp_assistant")
async def delete_temp_assistant(request: Request):
    data = await request.json()
    old_thread_id = decrypt_data(data.get('old_thread_id'))

    if not old_thread_id:
        return {"error": "Old thread ID is required."}

    assistant_info = assistant_cache.get(old_thread_id)
    if assistant_info:
        file_ids = assistant_info.get('file_ids', [])
        for file_id in file_ids:
            try:
                client.files.delete(file_id)
            except Exception as e:
                print(f"Error deleting file: {e}")

        try:
            client.beta.assistants.delete(assistant_info['assistant_id'])
        except Exception as e:
            print(f"Error deleting assistant: {e}")

        try:
            client.beta.vector_stores.delete(assistant_info['vector_store_id'])
        except Exception as e:
            print(f"Error deleting vector store: {e}")

        del assistant_cache[old_thread_id]

    return {"message": f"Switched from thread {old_thread_id}"}
