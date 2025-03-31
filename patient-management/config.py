# config.py
import os
from dotenv import load_dotenv
from datetime import timedelta


load_dotenv()  # Load environment variables from .env file if present


class Config:
    # Set the URI for the database. For simplicity, we use SQLite.
    API_TITLE = "Patient Management API"
    API_VERSION = "v1"
    OPENAPI_VERSION = "3.0.3"
    OPENAPI_URL_PREFIX = "/"
    OPENAPI_SWAGGER_UI_URL = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    OPENAPI_SWAGGER_UI_PATH = "/docs"
    OPENAPI_REDOC_PATH = "/redoc"
    OPENAPI_REDOC_URL = "https://cdn.jsdelivr.net/npm/redoc@next/bundles/redoc.standalone.js"
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY')  # For JWT encoding
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')  # For JWT encoding
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)