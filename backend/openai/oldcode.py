import os
import json
from dotenv import load_dotenv
from openai import OpenAI, AssistantEventHandler
from typing_extensions import override
from function_calling import get_moodle_course_content  # Ensure this function exists and works correctly

# Load environment variables
load_dotenv()
client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

class ToolEventHandler(AssistantEventHandler):
    def __init__(self):
        super().__init__()

    @override
    def on_text_created(self, text):
        # Do not print or accumulate text here to avoid duplication
        pass

    @override
    def on_text_delta(self, delta, snapshot):
        # Print incremental updates from tool outputs
        new_text = delta.value
        print(new_text, end='', flush=True)

# Define the assistant's event handler
class EventHandler(AssistantEventHandler):
    def __init__(self):
        super().__init__()
        self.current_output = ""

    @override
    def on_event(self, event):
        if event.event == 'thread.run.requires_action':
            run_id = event.data.id
            self.handle_requires_action(event.data, run_id)

    @override
    def on_text_created(self, text):
        # Do not print here to avoid duplication
        self.current_output += text.value

    @override
    def on_text_delta(self, delta, snapshot):
        # Print incremental updates
        new_text = delta.value
        self.current_output += new_text
        print(new_text, end='', flush=True)

    def handle_requires_action(self, data, run_id):
        tool_outputs = []
        for tool in data.required_action.submit_tool_outputs.tool_calls:
            if tool.function.name == "get_moodle_course_content":
                try:
                    arguments = json.loads(tool.function.arguments)
                    course_id = arguments.get("courseid", "51589")
                    result = get_moodle_course_content(course_id)
                    tool_outputs.append({
                        "tool_call_id": tool.id,
                        "output": result
                    })
                except (json.JSONDecodeError, ValueError) as e:
                    print(f"\nError processing course content: {e}")
                    tool_outputs.append({
                        "tool_call_id": tool.id,
                        "output": "Error fetching course content"
                    })
        self.submit_tool_outputs(tool_outputs, run_id)

    def submit_tool_outputs(self, tool_outputs, run_id):
        # Use a new ToolEventHandler instance
        with client.beta.threads.runs.submit_tool_outputs_stream(
            thread_id=self.current_run.thread_id,
            run_id=self.current_run.id,
            tool_outputs=tool_outputs,
            event_handler=ToolEventHandler(),  # New event handler instance
        ):
            pass  # Event handling is done in the event handler




def clean_up(assistant_id, thread_id, vector_store_id, file_ids):
    """Delete the assistant, thread, vector store, and uploaded files."""
    try:
        client.beta.assistants.delete(assistant_id)
        client.beta.threads.delete(thread_id)
        client.beta.vector_stores.delete(vector_store_id)
        for file_id in file_ids:
            client.files.delete(file_id)
        print("Resources cleaned up successfully.")
    except Exception as e:
        print(f"Error during cleanup: {e}")


FILES_DIR = "../data/"
file_ids = []

# Upload all files to OpenAI
for file in sorted(os.listdir(FILES_DIR)):
    try:
        _file = client.files.create(file=open(FILES_DIR + file, "rb"), purpose="assistants")
        file_ids.append(_file.id)
        print(f"Uploaded file: {_file.id} - {file}")
    except Exception as e:
        print(f"Error uploading file {file}: {e}")

# Create a vector store to store course content
try:
    vector_store = client.beta.vector_stores.create(
        name="Vorlesungsuntertitel zu den Grundlagen der Programmierung",
        file_ids=file_ids
    )
    print(f"Created vector store: {vector_store.id} - {vector_store.name}")
except Exception as e:
    print(f"Error creating vector store: {e}")
    clean_up(None, None, None, file_ids)
    exit()

instructions = (
    "Du bist ein freundlicher und unterstützender Lehrassistent für das Modul Grundlagen der Programmierung. "
    "Deine Aufgabe ist es, Erstsemester-Studierende zur Lösung zu führen, ohne jedoch vollständige Lösungen zu geben. "
    "Bespreche keine Themen, die nicht in den Vorlesungsskripten behandelt werden, wie zum Beispiel Listen. "
    "Deine Unterstützung soll das Verständnis fördern und das selbstständige Denken anregen, ohne die akademische "
    "Integrität zu gefährden. Verwende bei Bedarf nur Pseudocode im folgenden Format und kein richtiges Code: "
    "START\n"
    "    INITIALISIERE sum mit 0\n"
    "    FÜR jede Zahl von 1 bis 5 MACH\n"
    "        ADDIERE die Zahl zu sum\n"
    "    ENDE FÜR\n"
    "    GIB sum aus\n"
    "END"
)

# Register the assistant and add the Moodle function as a callable tool
try:
    assistant = client.beta.assistants.create(
        instructions=instructions,
        name="HTWCodingMentor",
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
                        },
                        "additionalProperties": False
                    }
                }
            },
            {
                "type": "file_search",
            }
        ],
        tool_resources={"file_search": {"vector_store_ids": [vector_store.id]}},
        model="gpt-4o-mini",
    )
    print(f"Created assistant: {assistant.id} - {assistant.name}")
except Exception as e:
    print(f"Error creating assistant: {e}")
    clean_up(None, None, vector_store.id, file_ids)
    exit()

# Start a conversation thread
try:
    thread = client.beta.threads.create()
except Exception as e:
    print(f"Error creating thread: {e}")
    clean_up(assistant.id, None, vector_store.id, file_ids)
    exit()

# ... [Your existing code above remains unchanged]

while True:
    user_input = input("User: ")
    if user_input.lower() in ["exit", "quit"]:
        print("Conversation ended.")
        break

    # Process the user input with the assistant
    try:
        thread_message = client.beta.threads.messages.create(
            thread.id,
            role="user",
            content=user_input
        )

        print(f"Running HTWCodingMentor: {assistant.id} in thread: {thread.id}")

        # Use a new EventHandler instance for each run
        with client.beta.threads.runs.stream(
            thread_id=thread.id,
            assistant_id=assistant.id,
            event_handler=EventHandler()  # Fresh EventHandler instance
        ) as stream:
            stream.until_done()  # Wait for the stream to finish
            print()
    except Exception as e:
        print(f"Error during assistant interaction: {e}")

# Clean up resources after the conversation ends
clean_up(assistant.id, thread.id, vector_store.id, file_ids)

