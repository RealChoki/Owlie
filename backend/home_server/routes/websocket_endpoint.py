import asyncio
import json
import os
import threading
from queue import Queue
from fastapi import WebSocket
from openai import OpenAI
from tools.fernet import decrypt_data
from tools.pii.pii_utils import presidio_anonymize, presidio_deanonymize
from handlers.event_handler import MyEventHandler
from queue import Queue

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
 
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            # Receive and parse client message
            data = await websocket.receive_text()
            try:
                payload = json.loads(data)
                thread_id = payload["thread_id"]
                assistant_id = payload["assistant_id"]
                message = payload["message"]
            except Exception as e:
                await websocket.send_text(f"Error: Invalid payload - {str(e)}")
                continue

            # Decrypt IDs
            try:
                decrypted_thread_id = decrypt_data(thread_id)
                decrypted_assistant_id = decrypt_data(assistant_id)
            except Exception as e:
                await websocket.send_text(f"Error: Decryption failed - {str(e)}")
                continue

            # Anonymize user message
            try:
                anonymized_message = presidio_anonymize(message)
            except Exception as e:
                await websocket.send_text(f"Error: Anonymization failed - {str(e)}")
                continue

            # Create user message in thread
            try:
                client.beta.threads.messages.create(
                    thread_id=decrypted_thread_id,
                    role="user",
                    content=anonymized_message
                )
            except Exception as e:
                await websocket.send_text(f"Error: Message creation failed - {str(e)}")
                continue

            # Create communication queue and event handler
            output_queue = Queue()
            handler = MyEventHandler(decrypted_thread_id, output_queue, client)  # Pass client

            # Stream processing thread
            def run_stream():
                try:
                    with client.beta.threads.runs.stream(
                        thread_id=decrypted_thread_id,
                        assistant_id=decrypted_assistant_id,
                        event_handler=handler,
                    ) as stream:
                        for chunk in stream:
                            if hasattr(chunk, "event") and chunk.event == "thread.message.delta":
                                for block in chunk.data.delta.content:
                                    if hasattr(block, "text"):
                                        try:
                                            deanonymized = presidio_deanonymize(block.text.value)
                                            output_queue.put(deanonymized)
                                        except Exception as e:
                                            output_queue.put(f"Error: Deanonymization failed - {str(e)}")
                    output_queue.put(None)
                except Exception as e:
                    output_queue.put(f"Error: Streaming failed - {str(e)}")
                    output_queue.put(None)

            stream_thread = threading.Thread(target=run_stream)
            stream_thread.start()

            # Stream results to client
            while True:
                item = await asyncio.to_thread(output_queue.get)
                if item is None:
                    await websocket.send_text("˘DONE˘")  # Send completion signal
                    break
                await websocket.send_text(item)
                
    except Exception as e:
        print(f"WebSocket error: {e}")
    finally:
        await websocket.close()
