import logging
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import API routers
from routes.courses import router as courses_router
from routes.thread import router as thread_router
from routes.websocket_endpoint import websocket_endpoint

# Configure logging
logging.basicConfig(level=logging.ERROR)

# Load environment variables
load_dotenv()

# Initialize FastAPI application
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include WebSocket route
app.add_api_websocket_route("/ws", websocket_endpoint)

# Include course-related endpoints
app.include_router(courses_router, prefix="/api")

# Include the thread-related endpoints
app.include_router(thread_router, prefix="/api")
