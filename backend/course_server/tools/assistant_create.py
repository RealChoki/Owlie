from pathlib import Path
import os
import uuid
import logging
from fastapi import APIRouter, HTTPException, File, Form, UploadFile
from pydantic import BaseModel
from dotenv import load_dotenv
from openai import OpenAI

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

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
        logger.info("Creating vector store...")
        file_ids = []
        # Upload any local files
        for file_name in files:
            file_path = Path("uploaded_files") / file_name
            if os.path.exists(file_path):
                logger.info(f"Uploading file: {file_name}")
                with open(file_path, "rb") as f:
                    uploaded = client.files.create(file=f, purpose="assistants")
                    file_ids.append(uploaded.id)
                    logger.info(f"Uploaded file ID: {uploaded.id}")

        # If there's transcribed text, upload it as an extra file
        if transcript:
            logger.info("Uploading transcript...")
            temp_transcript_path = "temp_transcript.txt"
            with open(temp_transcript_path, "w", encoding="utf-8") as tf:
                tf.write(transcript)
            with open(temp_transcript_path, "rb") as tf:
                uploaded_transcript = client.files.create(file=tf, purpose="assistants")
                file_ids.append(uploaded_transcript.id)
                logger.info(f"Uploaded transcript ID: {uploaded_transcript.id}")
            os.remove(temp_transcript_path)

        # Create vector store in OpenAI
        if not file_ids:
            logger.info("No files uploaded, returning UUID")
            return str(uuid.uuid4())
        logger.info("Creating vector store in OpenAI...")
        vector_store = client.beta.vector_stores.create(
            name="Assistant Vector Store",
            file_ids=file_ids
        )
        logger.info(f"Created vector store ID: {vector_store.id}")
        return vector_store.id
    except Exception as e:
        logger.error(f"Failed to create vector store: {e}")
        raise

moodle_instruction_path = Path(__file__).resolve().parent.parent / "instructions" / "moodle_tool.txt"

async def create_assistant(
    assistant_mode: str = Form(...),
    instructions: str = Form(...),
    transcribed_text: str = Form(...),
    moodle_enabled: str = Form("false"),
    files: list[UploadFile] = File([])
):
    try:
        logger.info("Creating assistant...")        
        upload_dir = "uploaded_files"
        os.makedirs(upload_dir, exist_ok=True)
        saved_filenames = []
        for uploaded_file in files:
            file_path = Path(upload_dir) / uploaded_file.filename
            logger.info(f"Saving file: {uploaded_file.filename}")
            with open(file_path, "wb") as f:
                f.write(await uploaded_file.read())
            saved_filenames.append(uploaded_file.filename)
        
        logger.info("Creating vector store...")
        vector_store_id = create_vector_store(saved_filenames, transcribed_text)

        tools = [
            {
                "type": "file_search",
            }
        ]

        if moodle_enabled.lower() == "true":
            with open(moodle_instruction_path, "r", encoding="utf-8") as f:
                moodle_text = f.read()

            kurs_name = "Advanced Python Programming"  # Example value
            kurs_id = "50115"  # Example value
            moodle_text = moodle_text.format(KURS_NAME=kurs_name, KURS_ID=kurs_id)
            instructions += "\n\n" + moodle_text
            logger.info("Adding Moodle tool...")
            tools.append(
                {
                    "type": "function",
                    "function": {
                        "name": "get_moodle_course_content",
                        "description": "Fetches Moodle course content based on course ID.",
                        "strict": True,
                        "parameters": {
                            "type": "object",
                            "required": ["courseid"],
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

        logger.info("Creating assistant in OpenAI...")
        assistant = client.beta.assistants.create(
            instructions=instructions,
            name=f"{assistant_mode} Assistant",
            tools=tools,
            tool_resources={"file_search": {"vector_store_ids": [vector_store_id]}},
            model="gpt-4o-mini"
        )
        logger.info(f"Created assistant ID: {assistant.id}")
        return {"assistant_id": assistant.id, "name": assistant.name}
    except Exception as e:
        logger.error(f"Error creating assistant: {e}")
        raise HTTPException(status_code=500, detail=str(e))