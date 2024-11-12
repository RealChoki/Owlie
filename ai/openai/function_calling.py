# function-calling.py
import os
import json
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Fetch the Moodle token from environment variables
moodle_token = os.getenv("MOODLE_TOKEN")

def get_moodle_course_content(courseid):
    """Fetches content for a specific Moodle course using the Moodle API."""
    moodle_call = (
        f'https://moodle.htw-berlin.de/webservice/rest/server.php?wstoken={moodle_token}'
        f'&wsfunction=core_course_get_contents&moodlewsrestformat=json&courseid={courseid}'
    )
    response = requests.get(moodle_call)
    response.raise_for_status()
    return json.dumps(response.json())
