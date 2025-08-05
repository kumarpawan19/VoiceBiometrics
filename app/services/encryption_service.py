from cryptography.fernet import Fernet
import os
from dotenv import load_dotenv

load_dotenv()
#ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY", Fernet.generate_key())  # Store securely
#cipher = Fernet(ENCRYPTION_KEY)

FERNET_KEY = os.getenv("FERNET_KEY")
cipher = Fernet(FERNET_KEY)

def encrypt_embedding(embedding):
    import numpy as np
    data = ",".join(map(str, embedding))  # convert array to string
    return cipher.encrypt(data.encode()).decode()

def decrypt_embedding(encrypted_str):
    decrypted = cipher.decrypt(encrypted_str.encode()).decode()
    return [float(x) for x in decrypted.split(",")]
