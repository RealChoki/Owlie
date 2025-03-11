import os
import logging
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI

# Import API routers
from routes.assistant import router as assistant_create_router
from routes.files import router as files_router
from routes.transcribe import router as transcribe_router

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

# Include the file manager endpoints
app.include_router(files_router, prefix="/api")

# Include course-related endpoints
app.include_router(transcribe_router, prefix="/api")

app.include_router(assistant_create_router, prefix="/api")


# validating	the input file is being validated before the batch can begin
# failed	the input file has failed the validation process
# in_progress	the input file was successfully validated and the batch is currently being run
# finalizing	the batch has completed and the results are being prepared
# completed	the batch has been completed and the results are ready
# expired	the batch was not able to be completed within the 24-hour time window
# cancelling	the batch is being cancelled (may take up to 10 minutes)
# cancelled	the batch was cancelled
