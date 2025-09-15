import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Database configuration
DB_HOST = os.getenv("DB_HOST")
DB_PORT = int(os.getenv("DB_PORT", 3306))
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

# App configuration
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
DEFAULT_JOB_STATUS = os.getenv("DEFAULT_JOB_STATUS", "active")
