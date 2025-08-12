import os
from dotenv import load_dotenv

# Load environment variables from .env file (useful for local dev)
load_dotenv()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# MongoDB URI (must be set in environment for production)
MONGO_URI = os.environ.get("MONGO_URI")
if not MONGO_URI:
    print("⚠️ WARNING: Using local MongoDB URI. Set MONGO_URI in environment for production.")
    MONGO_URI = "mongodb://localhost:27017/ictakpothole"

# MongoDB Database Name
MONGO_DB_NAME = os.environ.get("MONGO_DB_NAME", "ictakpothole")

# File Upload Configuration
UPLOAD_FOLDER = os.environ.get(
    "UPLOAD_FOLDER", os.path.join(BASE_DIR, "uploads"))
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "webp"}

# Secret Key (must be set in production)
SECRET_KEY = os.environ.get("SECRET_KEY")
if not SECRET_KEY:
    print("⚠️ WARNING: Using default SECRET_KEY. Set SECRET_KEY in environment for production.")
    SECRET_KEY = "dev_secret_key_change_in_prod"
