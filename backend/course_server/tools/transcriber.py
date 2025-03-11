from pathlib import Path
from transcribe_anything.api import transcribe
from tools.name_sanitizer import sanitize_filename

def transcribe_lecture(url_or_file: str, output_dir: str) -> str:
    # Run the transcription
    directory = Path(transcribe(
        url_or_file=url_or_file,
        output_dir=output_dir,
    ))

    print(f"Transcription saved in: {directory}")

    # Ensure the directory exists
    if not directory.exists():
        raise Exception(f"Directory {directory} does not exist.")

    # Check if transcription creates a subfolder
    subdirs = [item.name for item in directory.iterdir()]
    print(f"Contents of directory: {subdirs}")

    if len(subdirs) == 1 and (directory / subdirs[0]).is_dir():
        directory = directory / subdirs[0]  # Enter subfolder if necessary
        print(f"Updated directory path: {directory}")

    # Remove all non-.txt files
    txt_files = []
    for file in directory.iterdir():
        if file.suffix == ".txt":
            txt_files.append(file)  # Collect the .txt file path
        else:
            file.unlink()  # Delete non-txt files
            print(f"Deleted: {file.name}")

    # Ensure there is exactly one .txt file
    if not txt_files:
        raise Exception("No .txt file found in the transcription output.")
    
    old_txt_file_path = txt_files[0]  # The existing transcription file (e.g., "out.txt")

    # Generate a new filename with timestamp
    sanitized_url = sanitize_filename(url_or_file)
    new_file_name = f"{sanitized_url}.txt"
    new_txt_file_path = directory / new_file_name

    # Rename the .txt file
    old_txt_file_path.rename(new_txt_file_path)
    print(f"Renamed {old_txt_file_path} -> {new_txt_file_path}")

    # Read and return the transcription text
    return new_txt_file_path.read_text(encoding="utf-8")
