from fastapi import APIRouter
from fastapi import Form, File, UploadFile
from tools.assistant_create import create_assistant

router = APIRouter()

@router.post("/assistants/create")
async def create_assistant_endpoint(
    assistant_mode: str = Form(...),
    instructions: str = Form(...),
    transcribed_text: str = Form(""),
    moodle_enabled: str = Form("false"),
    files: list[UploadFile] = File([])
):
    return await create_assistant(
        assistant_mode=assistant_mode,
        instructions=instructions,
        transcribed_text=transcribed_text,
        moodle_enabled=moodle_enabled,
        files=files
    )