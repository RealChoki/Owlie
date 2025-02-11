from transcribe_anything.api import transcribe

transcribe(
    url_or_file="https://mediathek.htw-berlin.de/video/hallo-welt-unser-erstes-java-programm/07577ab0abe0206e22d3984082640842",
    output_dir="output_dir",
    language="german",
)