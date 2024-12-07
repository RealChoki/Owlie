import os
from cryptography.fernet import Fernet
from dotenv import load_dotenv

load_dotenv()

# # Generate a new key
# key = Fernet.generate_key()
# print(f"Secret key: {key.decode()}")

# Load the secret key from the environment
SECRET_KEY = os.getenv("FERNET_ENCRYPTION_KEY")
fernet = Fernet(SECRET_KEY)

def encrypt_data(data: str) -> str:
    """Encrypts data using Fernet symmetric encryption."""
    return fernet.encrypt(data.encode()).decode()

def decrypt_data(data: str) -> str:
    """Decrypts data using Fernet symmetric encryption."""
    return fernet.decrypt(data.encode()).decode()