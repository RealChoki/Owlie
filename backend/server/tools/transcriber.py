import os
import time
from transcribe_anything.api import transcribe

def transcribe_lecture(url_or_file: str, output_dir: str) -> str:
    # Run the transcription
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

    # Remove all non-.txt files
    txt_files = []
    for file in os.listdir(directory):
        file_path = os.path.join(directory, file)
        if file.endswith(".txt"):
            txt_files.append(file_path)  # Collect the .txt file path
        else:
            os.remove(file_path)  # Delete non-txt files
            print(f"Deleted: {file}")

    # Ensure there is exactly one .txt file
    if not txt_files:
        raise Exception("No .txt file found in the transcription output.")
    
    old_txt_file_path = txt_files[0]  # The existing transcription file (e.g., "out.txt")

    # Generate a new filename with timestamp
    new_file_name = f"lecture_{int(time.time())}.txt"
    new_txt_file_path = os.path.join(directory, new_file_name)

    # Rename the .txt file
    os.rename(old_txt_file_path, new_txt_file_path)
    print(f"Renamed {old_txt_file_path} -> {new_txt_file_path}")

    # Read and return the transcription text
    with open(new_txt_file_path, "r", encoding="utf-8") as file:
        return file.read()
