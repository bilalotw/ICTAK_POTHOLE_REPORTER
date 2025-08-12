import os
from dotenv import load_dotenv

# Load variables from .env (only needed locally)
load_dotenv()

# Base directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# MongoDB URI — MUST include the DB name at the end
MONGO_URI = os.environ.get("MONGO_URI")
if not MONGO_URI:
    # Fallback for local dev
    MONGO_URI = "mongodb://localhost:27017/ictakpothole"
    print("⚠️ WARNING: Using local MongoDB URI. Set MONGO_URI in environment for production.")

# Upload configuration
UPLOAD_FOLDER = os.environ.get(
    "UPLOAD_FOLDER", os.path.join(BASE_DIR, "uploads"))
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "webp"}

# Flask secret key
SECRET_KEY = os.environ.get("SECRET_KEY")
if not SECRET_KEY:
    SECRET_KEY = "dev_secret_key_change_in_prod"
    print("⚠️ WARNING: Using default SECRET_KEY. Set SECRET_KEY in environment for production.")
