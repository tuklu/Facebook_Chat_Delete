from cryptography.fernet import Fernet
import json
import os

# Function to generate and save the encryption key
def generate_key(file_path="secret.key"):
    key = Fernet.generate_key()
    with open(file_path, "wb") as key_file:
        key_file.write(key)

# Function to load the encryption key from a file
def load_key(file_path="secret.key"):
    if not os.path.exists(file_path):
        raise FileNotFoundError("Key file not found! Generate a key first.")
    with open(file_path, "rb") as key_file:
        return key_file.read()

# Function to encrypt a single string
def encrypt(data, key):
    cipher = Fernet(key)
    return cipher.encrypt(data.encode()).decode()

# Function to decrypt a single string
def decrypt(encrypted_data, key):
    cipher = Fernet(key)
    return cipher.decrypt(encrypted_data.encode()).decode()

# Function to encrypt credentials
def encrypt_credentials(username, password, key):
    return encrypt(username, key), encrypt(password, key)

# Function to decrypt credentials
def decrypt_credentials(encrypted_username, encrypted_password, key):
    return decrypt(encrypted_username, key), decrypt(encrypted_password, key)

# Save encrypted credentials to a file
def save_encrypted_credentials(username, password, key, file_path="credentials.json"):
    encrypted_username, encrypted_password = encrypt_credentials(username, password, key)
    credentials = {
        'username': encrypted_username,
        'password': encrypted_password
    }
    with open(file_path, "w") as cred_file:
        json.dump(credentials, cred_file)

# Load encrypted credentials from a file and decrypt
def load_and_decrypt_credentials(key, file_path="credentials.json"):
    if not os.path.exists(file_path):
        raise FileNotFoundError("Credentials file not found!")
    
    with open(file_path, "r") as cred_file:
        encrypted_credentials = json.load(cred_file)

    encrypted_username = encrypted_credentials['username']
    encrypted_password = encrypted_credentials['password']

    return decrypt_credentials(encrypted_username, encrypted_password, key)

# Function to get credentials
def get_credentials():
    try:
        key = load_key()  # Load the key from "secret.key"
        username, password = load_and_decrypt_credentials(key)
        return username, password
    except (FileNotFoundError, KeyError) as e:
        print(f"Error loading credentials: {e}")
        return None, None
