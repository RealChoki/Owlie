# general_assistant.py

import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def initialize_general_assistant():
    FILES_DIR = os.path.join(os.path.dirname(__file__), 'general data')
    file_ids = []

    # Iterate through all files in the 'general data' directory
    for file_name in os.listdir(FILES_DIR):
        file_path = os.path.join(FILES_DIR, file_name)
        if os.path.isfile(file_path):  # Ensure it's a file
            with open(file_path, "rb") as f:
                _file = client.files.create(file=f, purpose="assistants")
                file_ids.append(_file.id)
                print(f"Uploaded file for general mode: {_file.id} - {file_name}")

    # Create a vector store for the general assistant
    vector_store = client.beta.vector_stores.create(
        name="General Assistant Vector Store",
        file_ids=file_ids
    )
    vector_store_id = vector_store.id

    # Instructions for the general assistant
    instructions = (
        "Du bist ein interaktiver Mentor für Programmierkonzepte. Stelle eine Frage nach der anderen in vorgegebener "
        "Reihenfolge. Bei Schwierigkeiten stelle gezielte Fragen oder gib Erklärungen und Beispiele. Wiederhole Themen, "
        "bei denen der Benutzer unsicher ist, und überprüfe das Verständnis mit Kontrollfragen. Gratuliere bei Erfolg "
        "und gib Aufgaben zu Themen wo der benutzer schwierigkeiten hat. Dokumentiere behandelte und offene Themen klar. "
        "Beantworte ausschließlich Fragen zu Grundlagen der Programmierung oder Informatik. "
        "Wenn der Benutzer ein Thema nennt, zu dem er evaluiert werden möchte, führe ihn durch spezifische Fragen zu diesem Thema "
        "nur mit Hilfe bereitgestellter Fragen. Verhalte dich dabei wie eine weise Eule: freundlich und prägnant."
    )

    # Create the general assistant
    assistant = client.beta.assistants.create(
        instructions=instructions,
        name="HTWTestingAssistant",
        tools=[
            {
                "type": "function",
                "function": {
                    "name": "get_moodle_course_content",
                    "description": "Fetches Moodle course content based on course ID.",
                    "parameters": {
                        "type": "object",
                        "required": ["courseid"],
                        "properties": {
                            "courseid": {
                                "type": "string",
                                "description": "The Moodle course ID, e.g., '51589'."
                            }
                        }
                    }
                }
            }
        ],
        tool_resources={"file_search": {"vector_store_ids": [vector_store_id]}},
        model="gpt-4o-mini",
    )
    assistant_id = assistant.id
    print(f"Created general assistant: {assistant_id}")

    return assistant_id, vector_store_id, file_ids