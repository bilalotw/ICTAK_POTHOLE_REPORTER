import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Use MongoDB Atlas URI if provided in environment variables, otherwise fall back to local
MONGO_URI = os.environ.get(
    "MONGO_URI",
    "mongodb+srv://bilalapple247:NqI0xP6dizPUqhun@ictakpothole.8cxe46e.mongodb.net/?retryWrites=true&w=majority&appName=ictakpothole"
)

UPLOAD_FOLDER = os.environ.get(
    "UPLOAD_FOLDER", os.path.join(BASE_DIR, "uploads"))
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "webp"}

SECRET_KEY = os.environ.get("SECRET_KEY", "change_this_secret_in_prod")
