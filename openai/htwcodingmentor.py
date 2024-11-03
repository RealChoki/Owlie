import os
from dotenv import load_dotenv
load_dotenv()

from openai import OpenAI
from openai import AssistantEventHandler
from typing_extensions import override  # Import override decorator if needed
client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

class EventHandler(AssistantEventHandler):
    @override
    def on_text_created(self, text) -> None:
        print(f"\nAssistant: ", end="", flush=True)

    @override
    def on_text_delta(self, delta, snapshot):
        print(delta.value, end="", flush=True)

    def on_tool_call_created(self, tool_call):
        print(f"\nTool call created: {tool_call}")

    def on_tool_call_delta(self, delta, snapshot):
        print(f"\nTool call delta: {delta}")
        if delta.type == 'code_interpreter':
            if delta.code_interpreter.input:
                print(delta.code_interpreter.input, end="", flush=True)
            if delta.code_interpreter.outputs:
                print(f"\n\noutput >", flush=True)
                for output in delta.code_interpreter.outputs:
                    if output.type == "logs":
                        print(f"\n{output.logs}", flush=True)

def clean_up(assistant_id, thread_id, vector_store_id, file_ids):
    """Delete the assistant, thread, vector store, and uploaded files. """
    client.beta.assistants.delete(assistant_id)
    client.beta.threads.delete(thread_id)
    client.beta.vector_stores.delete(vector_store_id)
    [client.files.delete(file_id) for file_id in file_ids]

FILES_DIR = "../data/"
file_ids = []

for file in sorted(os.listdir(FILES_DIR)):
    _file = client.files.create(file=open(FILES_DIR + file, "rb"), purpose="assistants")
    file_ids.append(_file.id)
    print(f"Uploaded file: {_file.id} - {file}")

vector_store = client.beta.vector_stores.create(
  name="Vorlesungsuntertitel zu den Grundlagen der Programmierung",
  file_ids=file_ids
)
print(f"Created vector store: {vector_store.id} - {vector_store.name}")

instructions = (
    "Du bist HTWCodingMentor, ein freundlicher und hilfsbereiter Mentor für den 'Grundlagen der Programmierung'-Kurs an der HTW Berlin."
    "Du bist dabei auch ein Hund, was dich besonders sympathisch macht."
    "Deine Aufgabe ist es, Fragen zu den Grundlagen der Programmierung und Informatik auf einfache Weise zu beantworten und ausschließlich Pseudocode bereitzustellen."
    "1. Kursfokus: Beantworte nur Fragen, die sich auf den Grundlagenkurs der Programmierung und Informatik beziehen."
    "2. Keine irrelevanten Themen: Verzichte darauf, Fragen zu irrelevanten Themen zu beantworten."
    "3. Keine vollständigen Lösungen: Gib keine vollständigen Lösungen für Programmierprobleme, da dies die akademische Ehrlichkeit verletzen könnte."
    "4. Gedankenprozess abwarten: Lass die Studierenden zunächst ihr Verständnis des Problems darlegen. Stelle klärende Fragen, um ihre Denkprozesse zu unterstützen."
    "5. Einzelne Fragen: Stelle nur eine Frage auf einmal. Beginne mit dem ersten Thema und der ersten Frage. Gehe der Reihe nach vor."
    "6. Leitende Fragen: Wenn der Benutzer die Frage nicht vollständig beantworten kann, führe ihn sanft zur Antwort. Verwende gezielte Fragen, um ihm zu helfen, seine Gedanken zu klären."
    "7. Erklärungen und Übungen: Falls der Benutzer die Frage nicht beantworten kann, gib ihm Erklärungen und Beispiele, gefolgt von Übungen, die ihm helfen, das Konzept zu verstehen."
    "8. Interaktive Unterstützung: Interagiere aktiv mit dem Benutzer, bis er oder sie die Fragen zu den Themen eigenständig beantworten kann. Halte fest, bei welchen Themen der Benutzer Schwierigkeiten hat."
    "9. Wiederholung bei Schwierigkeiten: Nachdem alle Themen besprochen wurden, stelle dem Benutzer Fragen zu den Themen, bei denen er Schwierigkeiten hatte, um sein Verständnis zu überprüfen."
    "10. Lob und Aufgaben: Gratuliere dem Benutzer, wenn er ein Thema erfolgreich abschließt. Gib gezielte Aufgaben für Themen, bei denen er Schwierigkeiten hatte, bis er diese sicher beherrscht."
    "11. Themenverfolgung: Liste die behandelten Themen für die Woche auf und kennzeichne die erledigten Themen klar."
    "12. Themenbasierte Tests: Reagiere auf spezifische Eingaben wie 'Test Woche zwei' oder 'Test Methoden' und beginne mit einer Serie von Fragen zu den entsprechenden Kursinhalten."
    "13. Pseudocode-Leitfaden: Biete bei Bedarf abstrakte Pseudocode-Anleitungen an, um das Denken zu fördern. Nutze dabei dieses Format für Pseudocode:"
    "   START"
    "       INITIALISIERE sum mit 0"
    "       FÜR jede Zahl von 1 bis 5 MACH"
    "           ADDIERE die Zahl zu sum"
    "       ENDE FÜR"
    "       GIB sum aus"
    "   END"
)
assistant = client.beta.assistants.create(
    instructions=instructions,
    name="HTWCodingMentor",
    tools=[{"type": "file_search"}],
    tool_resources={"file_search": {"vector_store_ids": [vector_store.id]}},
    model="gpt-4o-mini",
)
print(f"Created assistant: {assistant.id} - {assistant.name}")

thread = client.beta.threads.create()

while True:
    user_input = input("User: ")
    if user_input.lower() in ["exit", "quit"]:
        print("Conversation ended.")
        break

    # Process the user input with the assistant
    thread_message = client.beta.threads.messages.create(
        thread.id,
        role="user",
        content=user_input
    )

    print(f"Running HTWCodingMentor: {assistant.id} in thread: {thread.id}")
    with client.beta.threads.runs.stream(
        thread_id=thread.id,
        assistant_id=assistant.id,
        event_handler=EventHandler()
    ) as stream:
        stream.until_done()
        print()

clean_up(assistant.id, thread.id, vector_store.id, file_ids)