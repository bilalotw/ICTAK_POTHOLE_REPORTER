import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Use MongoDB Atlas URI if provided in environment variables, otherwise fall back to local
MONGO_URI = os.environ.get(
    "MONGO_URI",
    "mongodb+srv://bilalapple247:gJ6ooYDPj0aSvplT@cluster0.ujq1txa.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
)

UPLOAD_FOLDER = os.environ.get(
    "UPLOAD_FOLDER", os.path.join(BASE_DIR, "uploads"))
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "webp"}

SECRET_KEY = os.environ.get("SECRET_KEY", "change_this_secret_in_prod")
