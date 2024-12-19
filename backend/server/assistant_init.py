# backend/server/assistant_init.py

import os
import json
from dotenv import load_dotenv
from openai import OpenAI
import logging

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Get the directory of the current script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Construct the path to 'config.json' one level up
config_path = os.path.join(BASE_DIR, '..', 'config.json')

# Load and parse config.json
with open(config_path, 'r') as f:
    config_data = json.load(f)

def get_course_config(course_name, mode_name):
    # Traverse the config to find the matching course and mode
    for university in config_data['universities'].values():
        for degree_level in university.values():
            for subject in degree_level.values():
                course = subject.get(course_name)
                if course and mode_name in course:
                    return course[mode_name]
    raise ValueError('Course or mode not found in config')

def initialize_assistant(course_name, mode_name):
    try:
        mode_config = get_course_config(course_name, mode_name)
        instructions = mode_config['instructions']
        data_path = mode_config['data_path']
        tools = mode_config['tools']
        model = mode_config['model']

        # Get existing assistant_id and vector_store_id if they exist
        assistant_id = mode_config.get('assistant_id')
        vector_store_id = mode_config.get('vector_store_id')

        # Check if the vector store exists
        if not vector_store_id:
            # Upload files and create vector store as before
            FILES_DIR = os.path.abspath(os.path.join(BASE_DIR, '..', data_path))
            if not os.path.exists(FILES_DIR):
                raise FileNotFoundError(f"Data path {FILES_DIR} does not exist.")

            file_ids = []
            for file in sorted(os.listdir(FILES_DIR)):
                file_path = os.path.join(FILES_DIR, file)
                if os.path.isfile(file_path):
                    with open(file_path, "rb") as f:
                        _file = client.files.create(file=f, purpose="assistants")
                        file_ids.append(_file.id)
                        print(f"Uploaded file: {_file.id} - {file}")
                else:
                    print(f"Skipping {file_path}, not a file.")

            if not file_ids:
                raise ValueError("No files were uploaded. Please check the data directory.")

            # Create vector store
            vector_store = client.beta.vector_stores.create(
                name=f"{course_name} - {mode_name}",
                file_ids=file_ids
            )
            vector_store_id = vector_store.id
            mode_config['vector_store_id'] = vector_store_id
            print(f"Created vector store: {vector_store_id} - {vector_store.name}")
        else:
            print(f"Using existing vector store: {vector_store_id}")

        # Now, update or create the assistant
        if assistant_id:
            # Assistant exists, attempt to update it
            print(f"Updating existing assistant: {assistant_id}")
            try:
                assistant = client.beta.assistants.update(
                    assistant_id=assistant_id,
                    instructions=instructions,
                    tools=tools,
                    tool_resources={"file_search": {"vector_store_ids": [vector_store_id]}},
                    model=model
                )
                print(f"Assistant updated: {assistant.id} - {assistant.name}")
            except Exception as e:
                logging.error(f"Error updating assistant: {e}")
                raise e
        else:
            # Assistant does not exist, create a new one
            print("Creating new assistant")
            assistant = client.beta.assistants.create(
                instructions=instructions,
                name=f"{course_name} - {mode_name} Assistant",
                tools=tools,
                tool_resources={"file_search": {"vector_store_ids": [vector_store_id]}},
                model=model,
            )
            assistant_id = assistant.id
            mode_config['assistant_id'] = assistant_id
            print(f"Created assistant: {assistant_id} - {assistant.name}")

        # Update config.json with any changes
        with open(config_path, 'w') as f:
            json.dump(config_data, f, indent=4)

        print(f"Assistant initialized and config.json updated.")
    except Exception as e:
        logging.error(f"Error initializing assistant: {e}")
        raise e

if __name__ == "__main__":
    # Corrected course name with proper capitalization
    course_name = "Grundlagen_der_Programmierung"
    mode_name = "quiz"
    initialize_assistant(course_name, mode_name)