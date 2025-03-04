import re

def sanitize_filename(url: str) -> str:
    # Remove the protocol part (http:// or https://)
    url = re.sub(r'^https?:\/\/', '', url)
    # Replace any character that is not alphanumeric or an underscore with an underscore
    return re.sub(r'[^a-zA-Z0-9_]', '_', url)