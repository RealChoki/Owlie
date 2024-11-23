# HTW Coding Mentor Chatbot API

A **FastAPI-powered** backend for an AI-driven coding mentor, aiding students with programming fundamentals through an interactive chat experience.

## Features
- **AI Chat Assistant**: Tailored programming guidance.
- **Moodle Integration**: Fetches course content.
- **Persistent Conversations**: Stores and retrieves chat histories.
- **Extensible**: Easily add new tools or capabilities.

## Setup

### Requirements
- Python 3.8+
- FastAPI
- OpenAI API Key

### Installation
1. **Clone the repository**:
     ```bash
     git clone https://github.com/yourusername/HTW-Coding-Mentor-Chatbot.git
     cd HTW-Coding-Mentor-Chatbot
     ```
2. **Install dependencies**:
     ```bash
     pip install -r requirements.txt
     ```
3. **Environment setup**: Create a `.env` file with your OpenAI API Key:
     ```
     OPENAI_API_KEY=your_openai_api_key
     ```
4. **Run the Server**: Start the FastAPI server:
     ```bash
     uvicorn fastapiserver:app --reload --host 0.0.0.0 --port 8000
     ```

## API Endpoints

### Create a New Conversation
**POST /api/new**: Initializes a new chat thread.
- **Response**: Returns `run_id` and `thread_id`.

### Send a Message
**POST /api/threads/{thread_id}**: Sends a message to an existing thread.
- **Parameters**: `thread_id` (Path)
- **Body**:
  ```json
  {
      "content": "Your message here"
  }
  ```
- **Response**: Status of the AI's response.

### Retrieve Conversation History
**GET /api/threads/{thread_id}**: Fetches all messages in the specified thread.
- **Parameters**: `thread_id` (Path)
- **Response**: List of messages with roles and timestamps.

### Check AI Response Status
**GET /api/threads/{thread_id}/runs/{run_id}**: Retrieves the status of the AI's response.
- **Parameters**: `thread_id` (Path), `run_id` (Path)
- **Response**: Current status of the AI response.

### Submit Tool Outputs
**POST /api/threads/{thread_id}/runs/{run_id}/tool**: Submits tool outputs required by the AI.
- **Parameters**: `thread_id` (Path), `run_id` (Path)
- **Body**:
  ```json
  [
      {
          "tool_call_id": "example_tool_call_id",
          "output": "Example output"
      }
  ]
  ```
- **Response**: Status update on the tool output submission.

## Usage Example

### Start a Conversation
**Request**: POST /api/new
**Response**:
```json
{
  "run_id": "run_xxx",
  "thread_id": "thread_xxx",
  "status": "queued",
  "required_action": null,
  "last_error": null
}
```

### Send a Message
**Request**: POST /api/threads/thread_xxx
**Body**:
```json
{
  "content": "Hello, can you help me with loops in Python?"
}
```
**Response**:
```json
{
  "run_id": "run_yyy",
  "thread_id": "thread_xxx",
  "status": "queued",
  "required_action": null,
  "last_error": null
}
```

### Retrieve Chat History
**Request**: GET /api/threads/thread_xxx
**Response**:
```json
{
  "messages": [
      {
          "content": "Hallo! Ich bin dein freundlicher Lehrassistent...",
          "role": "assistant",
          "hidden": false,
          "id": "msg_xxx",
          "created_at": 1732383966
      },
      {
          "content": "Greet the user and tell them about yourself...",
          "role": "user",
          "hidden": true,
          "id": "msg_yyy",
          "created_at": 1732383965
      }
  ]
}
```