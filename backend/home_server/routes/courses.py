import json
from fastapi import APIRouter, HTTPException
from tools.fernet import encrypt_data
from tools.config_loader import get_assistant_ids
from pathlib import Path

config_path = Path(__file__).resolve().parent.parent / "config.json"

# Load and parse config.json y
with open(config_path, 'r') as f:
    config_data = json.load(f)
router = APIRouter()

@router.get("/courses")
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

@router.get("/get_assistant_ids")
async def get_assistant_ids_endpoint(course_name: str, mode_name: str):
    try:
        assistant_id = get_assistant_ids(course_name, mode_name)
        
        # Encrypt the assistant_id before returning it
        encrypted_assistant_id = encrypt_data(assistant_id)
        
        return {"assistant_id": encrypted_assistant_id}
    except ValueError as e:
        return {"error": str(e)}
