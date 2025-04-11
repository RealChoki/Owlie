import os
from openai import OpenAI
from fastapi import HTTPException, Request, APIRouter
from pydantic import BaseModel
from openai.types.beta.threads.run import LastError, RequiredAction
from typing import List, Optional
from tools.fernet import decrypt_data, encrypt_data

router = APIRouter()

# Import the functions from your file
from tools.fernet import decrypt_data

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
thread_moodle_cache = {}

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

@router.post("/threads/{thread_id}/runs/{run_id}/cancel")
async def stop_thread(thread_id: str, run_id: str):
    # Decrypt the thread_id
    decrypted_thread_id = decrypt_data(thread_id)

    print(f"Stopping thread: {decrypted_thread_id}")
    # Stop the thread
    client.beta.threads.runs.cancel(run_id=run_id,thread_id=decrypted_thread_id)
    # print(client.beta.threads.runs.cancel(run_id=run_id,thread_id=decrypted_thread_id))
    return {"message": "Thread stopped successfully."}

# Update endpoints to check if assistant_id is initialized d
@router.post("/new")
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

@router.get("/threads/{thread_id}")
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

@router.get("/runs/{thread_id}/{run_id}")
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