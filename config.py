import os, sys
from dotenv import load_dotenv


def resource_path(relative_path):
    """Return absolute path to resource, works for dev and PyInstaller bundle"""
    base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

# Load environment variables from .env
env_path = resource_path(".env")
load_dotenv(env_path)

# Database configuration
DB_HOST = os.getenv("DB_HOST")
DB_PORT = int(os.getenv("DB_PORT", 3306))
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME") #Stage Tracker database
DB_NAME_ASSETMANAGER = os.getenv("DB_NAME_ASSETMANAGER") #Assetmanager database

# App configuration
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
DEFAULT_JOB_STATUS = os.getenv("DEFAULT_JOB_STATUS", "active")
