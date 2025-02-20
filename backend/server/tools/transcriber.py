import os
from transcribe_anything.api import transcribe

def transcribe_lecture(url_or_file: str) -> str:
    output_dir = "output_dir"
    directory = transcribe(
        url_or_file=url_or_file,
        output_dir=output_dir,
    )
    
    print(f"Transcription saved in: {directory}")
    
    # Ensure the directory exists
    if not os.path.exists(directory):
        raise Exception(f"Directory {directory} does not exist.")
    
    # Check if transcription creates a subfolder
    subdirs = os.listdir(directory)
    print(f"Contents of directory: {subdirs}")
    
    if len(subdirs) == 1 and os.path.isdir(os.path.join(directory, subdirs[0])):
        directory = os.path.join(directory, subdirs[0])  # Enter subfolder if necessary
        print(f"Updated directory path: {directory}")

    # List files and filter for .txt files
    txt_files = [f for f in os.listdir(directory) if f.endswith('.txt')]
    
    if not txt_files:
        raise Exception("No .txt file found in the transcription output.")
    
    txt_file_path = os.path.join(directory, txt_files[0])
    print(f"Using text file: {txt_file_path}")
    
    with open(txt_file_path, "r", encoding="utf-8") as file:
        return file.read()
