import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MONGO_URI = os.environ.get("MONGO_URI", "mongodb://localhost:27017/pothole_db")
UPLOAD_FOLDER = os.environ.get("UPLOAD_FOLDER", os.path.join(BASE_DIR, "uploads"))
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "webp"}

SECRET_KEY = os.environ.get("SECRET_KEY", "change_this_secret_in_prod")
