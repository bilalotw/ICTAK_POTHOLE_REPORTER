import os
from dotenv import load_dotenv  # Add this import

# Load environment variables from .env file
load_dotenv()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# MongoDB Configuration - ONLY use environment variables
MONGO_URI = os.environ["MONGO_URI"]  # No fallback value!
DB_NAME = os.environ.get("MONGO_DB_NAME", "default_db")

# File Uploads
UPLOAD_FOLDER = os.environ.get(
    "UPLOAD_FOLDER", 
    os.path.join(BASE_DIR, "uploads")
)
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "webp"}

# Security
SECRET_KEY = os.environ["SECRET_KEY"]  # No default value!