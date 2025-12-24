from cryptography.fernet import Fernet
import os

ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY", Fernet.generate_key())
cipher = Fernet(ENCRYPTION_KEY)

def encrypt_password(password: str) -> str:
    return cipher.encrypt(password.encode()).decode()

def decrypt_password(encrypted: str) -> str:
    return cipher.decrypt(encrypted.encode()).decode()