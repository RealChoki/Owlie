from queue import Queue
from openai import AssistantEventHandler, OpenAI
from tools.moodle_tool import get_moodle_course_content

class MyEventHandler(AssistantEventHandler):
    def __init__(self, thread_id: str, output_queue: Queue, client: OpenAI):
        super().__init__()
        self.thread_id = thread_id
        self.output_queue = output_queue
        self.client = client

    def on_event(self, event):
        if event.event == "thread.run.requires_action":
            self.handle_requires_action(event.data, event.data.id)

    def handle_requires_action(self, data, run_id):
        tool_outputs = []
        for tool in data.required_action.submit_tool_outputs.tool_calls:
            if tool.function.name == "get_moodle_course_content":
                content = get_moodle_course_content(courseid="50726")
                tool_outputs.append({
                    "tool_call_id": tool.id,
                    "output": content
                })
        self.submit_tool_outputs(tool_outputs, run_id)

    def submit_tool_outputs(self, tool_outputs, run_id):
        try:
            new_handler = MyEventHandler(self.thread_id, self.output_queue, self.client)
            with self.client.beta.threads.runs.submit_tool_outputs_stream(
                thread_id=self.thread_id,
                run_id=run_id,
                tool_outputs=tool_outputs,
                event_handler=new_handler,
            ) as stream:
                for text in stream.text_deltas:
                    self.output_queue.put(text)
        except Exception as e:
            self.output_queue.put(f"Error: Tool processing failed - {str(e)}")
 