from pathlib import Path
from fastapi import HTTPException, APIRouter, Body
from tools.transcriber import transcribe_lecture

router = APIRouter()

@router.post("/transcribe_lecture")
async def transcribe_lecture_endpoint(
    lecture_url: str = Body(..., embed=True),
    university: str = Body(..., embed=True),
    course_id: str = Body(..., embed=True),
    mode: str = Body(..., embed=True),
):
    try:
        save_dir = Path("transcribed_lectures") / university / course_id / mode
        save_dir.mkdir(parents=True, exist_ok=True)  # Create directories if they don't exist

        text = transcribe_lecture(url_or_file=lecture_url, output_dir=str(save_dir))

        return text
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))