import os
import uuid
import logging
from fastapi import APIRouter, HTTPException, File, Form, UploadFile
from pydantic import BaseModel
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
router = APIRouter()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class AssistantCreateRequest(BaseModel):
    assistant_mode: str
    instructions: str
    transcribed_text: str
    files: list[str]  # List of file names (uploaded locally)

def create_vector_store(files: list[str], transcript: str) -> str:
    try:
        print("Creating vector store...")
        file_ids = []
        # Upload any local files
        for file_name in files:
            file_path = os.path.join("uploaded_files", file_name)
            if os.path.exists(file_path):
                print(f"Uploading file: {file_name}")
                with open(file_path, "rb") as f:
                    uploaded = client.files.create(file=f, purpose="assistants")
                    file_ids.append(uploaded.id)
                    print(f"Uploaded file ID: {uploaded.id}")

        # If there's transcribed text, upload it as an extra file
        if transcript:
            print("Uploading transcript...")
            temp_transcript_path = "temp_transcript.txt"
            with open(temp_transcript_path, "w", encoding="utf-8") as tf:
                tf.write(transcript)
            with open(temp_transcript_path, "rb") as tf:
                uploaded_transcript = client.files.create(file=tf, purpose="assistants")
                file_ids.append(uploaded_transcript.id)
                print(f"Uploaded transcript ID: {uploaded_transcript.id}")
            os.remove(temp_transcript_path)

        # Create vector store in OpenAI
        if not file_ids:
            print("No files uploaded, returning UUID")
            return str(uuid.uuid4())
        print("Creating vector store in OpenAI...")
        vector_store = client.beta.vector_stores.create(
            name="Assistant Vector Store",
            file_ids=file_ids
        )
        print(f"Created vector store ID: {vector_store.id}")
        return vector_store.id
    except Exception as e:
        logging.error(f"Failed to create vector store: {e}")
        raise

@router.post("/api/assistants/create")
async def create_assistant(
    assistant_mode: str = Form(...),
    instructions: str = Form(...),
    transcribed_text: str = Form(...),
    files: list[UploadFile] = File([])
):
    try:
        print("Creating assistant...")        
        upload_dir = "uploaded_files"
        os.makedirs(upload_dir, exist_ok=True)
        saved_filenames = []
        for uploaded_file in files:
            file_path = os.path.join(upload_dir, uploaded_file.filename)
            print(f"Saving file: {uploaded_file.filename}")
            with open(file_path, "wb") as f:
                f.write(await uploaded_file.read())
            saved_filenames.append(uploaded_file.filename)
        
        # Create vector store
        print("Creating vector store...")
        vector_store_id = create_vector_store(saved_filenames, transcribed_text)

        # Instead of a list of strings, we pass a list of objects:
        tools = [
            {
                "type": "file_search",
            }
        ]
        if "moodle" in assistant_mode.lower():
            print("Adding Moodle tool...")
            tools.append(
                {
                    "type": "function",
                    "function": {
                          "name": "get_moodle_course_content",
                            "description": "Fetches Moodle course content based on course ID.",
                            "strict": True,
                            "parameters": {
                                "type": "object",
                                "required": [
                                "courseid"
                                ],
                                "properties": {
                                "courseid": {
                                    "type": "string",
                                    "description": "The Moodle course ID, e.g., '50115'."
                                }
                                },
                                "additionalProperties": False
                            }
                    }
                }
            )
        print("Creating assistant in OpenAI...")
        assistant = client.beta.assistants.create(
            instructions=instructions,
            name=f"{assistant_mode} Assistant",
            tools=tools,
            tool_resources={"file_search": {"vector_store_ids": [vector_store_id]}},
            model="gpt-4o-mini"
        )
        print(f"Created assistant ID: {assistant.id}")
        return {"assistant_id": assistant.id, "name": assistant.name}
    except Exception as e:
        print(f"Error creating assistant: {e}")
        raise HTTPException(status_code=500, detail=str(e))