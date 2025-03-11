from fastapi import HTTPException, APIRouter, Request
from pathlib import Path
from tools.name_sanitizer import sanitize_filename

router = APIRouter()

TRANSCRIBED_FILES_DIR = Path(__file__).resolve().parent.parent / 'transcribed_lectures' / 'Harvard' / '66666' / 'general'
@router.get("/assistants/file/{filename}")
async def get_transcribed_file(filename: str):
    try:
        sanitized_filename = sanitize_filename(filename) + ".txt"
        filepath = TRANSCRIBED_FILES_DIR / sanitized_filename
        print(filepath)
        print(sanitized_filename)
        if not filepath.exists():
            raise FileNotFoundError(f"Quiz file not found: {filepath}")

        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        return {"title": sanitized_filename, "content": content}

    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/assistants/file/{filename}")
async def update_transcribed_file(filename: str, request: Request):
    try:
        # Read the updated content from the request
        content = await request.body()
        filepath = TRANSCRIBED_FILES_DIR / filename

        # Ensure the directory exists
        TRANSCRIBED_FILES_DIR.mkdir(parents=True, exist_ok=True)

        # Overwrite the file with new content
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content.decode("utf-8"))

        return {"message": f"Quiz file '{filename}' updated successfully."}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
