from pydantic_settings import BaseSettings
from pathlib import Path

# Define the path to the .env file in the outer_folder
env_path = Path(__file__).resolve().parent / ".env"  # Automatically points to .env in the same folder as app.py


class Settings(BaseSettings):
    database_hostname: str
    database_port: str
    database_password: str
    database_name: str
    database_username: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    class Config:
        env_file = env_path


settings = Settings()