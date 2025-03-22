from dotenv import load_dotenv
import os
import jwt
from datetime import datetime, timedelta


from pathlib import Path

# Define the path to the .env file in the outer_folder
env_path = Path(__file__).resolve().parent / ".env"  # Automatically points to .env in the same folder as app.py

# Load environment variables from the specified .env file
load_dotenv(dotenv_path=env_path)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")))
    to_encode.update({"exp":expire})
    encoded_jwt = jwt.encode(to_encode, os.getenv("SECRET_KEY"), algorithm=os.getenv("ALGORITHM"))
    return encoded_jwt
