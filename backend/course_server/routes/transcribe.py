import os
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

        save_dir = os.path.join("transcribed_lectures", university, course_id, mode)
        os.makedirs(save_dir, exist_ok=True)

        text = transcribe_lecture(url_or_file=lecture_url, output_dir=save_dir)

        return text
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))