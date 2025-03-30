# config.py
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file if present

print(os.getenv('SQLALCHEMY_DATABASE_URI')) 

class Config:
    # Set the URI for the database. For simplicity, we use SQLite.
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY')  # For JWT encoding

   