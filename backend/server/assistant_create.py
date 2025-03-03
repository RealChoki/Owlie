from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
router = APIRouter()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class AssistantCreateRequest(BaseModel):
    assistant_mode: str
    instructions: str
    transcribed_text: str
    files: list[str]  # list of file names (optional)

@router.post("/api/assistants/create")
async def create_assistant(payload: AssistantCreateRequest):
    try:
        # Here you can use payload.transcribed_text and payload.files as needed
        # For this example we simply use the instructions from the frontend
        assistant = client.beta.assistants.create(
            instructions=payload.instructions,
            name=f"{payload.assistant_mode} Assistant",
            tools=["file_search"],
            tool_resources={"file_search": {"vector_store_ids": []}},  # adjust if vector store available
            model="gpt-4"  # or use another model as needed
        )
        return {"assistant_id": assistant.id, "name": assistant.name}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
