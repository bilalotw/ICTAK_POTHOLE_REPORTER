import os
from dotenv import load_dotenv

# Load .env file (only in local dev, doesn't harm in production)
load_dotenv()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# MongoDB URI
MONGO_URI = os.environ.get(
    "MONGO_URI",
    "mongodb://localhost:27017/pothole_db"
)
if "MONGO_URI" not in os.environ:
    print("⚠️ WARNING: Using local MongoDB URI. Set MONGO_URI in environment for production.")

# MongoDB Database Name
DB_NAME = os.environ.get("MONGO_DB_NAME", "ictakpothole")

# File Upload Configuration
UPLOAD_FOLDER = os.environ.get("UPLOAD_FOLDER", os.path.join(BASE_DIR, "uploads"))
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "webp"}

# Security Key
SECRET_KEY = os.environ.get("SECRET_KEY", "dev_secret_key_change_in_prod")
if SECRET_KEY == "dev_secret_key_change_in_prod":
    print("⚠️ WARNING: Using default SECRET_KEY. Set SECRET_KEY in environment for production.")
