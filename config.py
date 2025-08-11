import os
from dotenv import load_dotenv  # Add this import

# Load environment variables from .env file
load_dotenv()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

<<<<<<< HEAD
# MongoDB Configuration - ONLY use environment variables
MONGO_URI = os.environ["MONGO_URI"]  # No fallback value!
DB_NAME = os.environ.get("MONGO_DB_NAME", "default_db")
=======
# Use MongoDB Atlas URI if provided in environment variables, otherwise fall back to local
MONGO_URI = os.environ.get(
    "MONGO_URI",
    "mongodb+srv://bilalapple247:NqI0xP6dizPUqhun@ictakpothole.8cxe46e.mongodb.net/?retryWrites=true&w=majority&appName=ictakpothole"
)
>>>>>>> ea1b327f98837e53fc7bbd430263aac55c8124e1

# File Uploads
UPLOAD_FOLDER = os.environ.get(
    "UPLOAD_FOLDER", 
    os.path.join(BASE_DIR, "uploads")
)
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "webp"}

# Security
SECRET_KEY = os.environ["SECRET_KEY"]  # No default value!