# not using, saving as fallback function if ws fails!

import threading
import asyncio
import os
from queue import Queue
from fastapi import FastAPI
from starlette.responses import StreamingResponse

# Import the functions from your file
from tools.pii.pii_utils import presidio_anonymize, presidio_deanonymize
from tools.fernet import decrypt_data
from handlers.event_handler import MyEventHandler
from openai import OpenAI

app = FastAPI()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.get("/api/threads/{thread_id}/stream")
async def send_and_stream(thread_id: str, assistant_id: str, message: str):
    # Decrypt the thread and assistant IDs.
    decrypted_thread_id = decrypt_data(thread_id)
    decrypted_assistant_id = decrypt_data(assistant_id)

    # Anonymize the user message before sending.
    print("Original user message:", message)
    anonymized_message = presidio_anonymize(message)
    print("Anonymized user message:", anonymized_message)

    # Send the anonymized message to the thread.
    client.beta.threads.messages.create(
        thread_id=decrypted_thread_id,
        role="user",
        content=anonymized_message
    )

    # Create a thread-safe queue to collect text deltas.
    output_queue = Queue()

    # Create our event handler instance with the shared output queue.
    handler = MyEventHandler(decrypted_thread_id, output_queue)

    # Define a function to run the synchronous stream in a separate thread.
    def run_stream():
        with client.beta.threads.runs.stream(
            thread_id=decrypted_thread_id,
            assistant_id=decrypted_assistant_id,
            event_handler=handler,
        ) as stream:
            for chunk in stream:
                # If the chunk is a text delta from the assistant, push it to the queue.
                if hasattr(chunk, "event") and chunk.event == "thread.message.delta":
                    delta_content = chunk.data.delta.content
                    for block in delta_content:
                        if hasattr(block, "text") and hasattr(block.text, "value"):
                            # De-anonymize the assistant's response.
                            print("Original assistant response:", block.text.value)
                            text_val = presidio_deanonymize(block.text.value)
                            print("De-anonymized assistant response:", text_val)
                            output_queue.put(text_val)
            # Signal end-of-stream by pushing a special marker (None).
            output_queue.put(None)

    # Use the threading module to run the blocking stream.
    stream_thread = threading.Thread(target=run_stream)
    stream_thread.start()

    # Define our async event generator that yields text from the output queue.
    async def event_generator():
        while True:
            # Get an item from the queue in a thread-safe way.
            item = await asyncio.to_thread(output_queue.get)
            if item is None:
                break
            yield item
            await asyncio.sleep(0)  # Yield control to the event loop.

    return StreamingResponse(event_generator(), media_type="text/event-stream")