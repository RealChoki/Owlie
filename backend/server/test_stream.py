import os
from openai import OpenAI

from typing_extensions import override
from openai import AssistantEventHandler

# First, we create a EventHandler class to define
# how we want to handle the events in the response stream.

class EventHandler(AssistantEventHandler):    
    @override
    def on_text_created(self, text) -> None:
        print(f"\nassistant > ", end="", flush=True)
        
    @override
    def on_text_delta(self, delta, snapshot):
        print(delta.value, end="", flush=True)
        
    def on_tool_call_created(self, tool_call):
        print(f"\nassistant > {tool_call.type}\n", flush=True)

    def on_tool_call_delta(self, delta, snapshot):
        if delta.type == 'code_interpreter':
            if delta.code_interpreter.input:
                print(delta.code_interpreter.input, end="", flush=True)
            if delta.code_interpreter.outputs:
                print(f"\n\noutput >", flush=True)
            for output in delta.code_interpreter.outputs:
                if output.type == "logs":
                    print(f"\n{output.logs}", flush=True)

# Initialize the OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
# Specify the ID of the existing assistant
existing_assistant_id = "asst_ITEK83NLc8Uigo2jTka6nUOt"

# Step 1: Retrieve the Existing Assistant
existing_assistant = client.beta.assistants.retrieve(existing_assistant_id)

# Step 2: Create a Thread
my_thread = 'thread_zRH7LVrHZU9sPWXqFFtd20Aw'

# Step 3: Add a Message to a Thread
my_thread_message = client.beta.threads.messages.create(
  thread_id=my_thread,
  role="user",
  content="Hey was ist java?",
)
print(f"This is the message object: {my_thread_message.id} \n")

# Step 4: Run the Assistant
my_run = client.beta.threads.runs.create(
  thread_id=my_thread,
  assistant_id=existing_assistant_id,
)
print(f"This is the run object: {my_run} \n")

# Step 5: Periodically retrieve the Run to check on its status to see if it has moved to completed
while my_run.status in ["queued", "in_progress"]:
    keep_retrieving_run = client.beta.threads.runs.retrieve(
        thread_id=my_thread,
        run_id=my_run.id
    )

    # with client.beta.threads.runs.stream(
    #     thread_id=my_thread,
    #     assistant_id=existing_assistant_id,
    #     event_handler=EventHandler(),
    # ) as stream:
    #     stream.until_done()

    print(f"Run retrival: {keep_retrieving_run}")

    if keep_retrieving_run.status == "completed":
        print("\n")

        # Step 6: Retrieve the Messages added by the Assistant to the Thread
        all_messages = client.beta.threads.messages.list(
            thread_id=my_thread
        )

        print("------------------------------------------------------------ \n")

        print(f"User: {my_thread_message.content[0].text.value}")
        print(f"Assistant: {all_messages.data[0].content[0].text.value}")

        break
    elif keep_retrieving_run.status == "queued" or keep_retrieving_run.status == "in_progress":
        pass
    else:
        print(f"Run status 2: {keep_retrieving_run.status}")
        break
