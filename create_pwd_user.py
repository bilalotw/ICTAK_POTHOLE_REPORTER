# create_pwd_user.py
# Helper script to create a PWD staff account in MongoDB.
# Usage: python create_pwd_user.py admin password

import sys
import os
from pymongo import MongoClient
from werkzeug.security import generate_password_hash

# Validate arguments
if len(sys.argv) < 3:
    print("Usage: python create_pwd_user.py <username> <password>")
    sys.exit(1)

username = sys.argv[1]
password = sys.argv[2]

# Load MongoDB config from env vars
mongo_uri = os.environ.get("MONGODB_URI", "mongodb://localhost:27017/")
db_name = os.environ.get("MONGODB_DB", "potholedb")

# Connect to MongoDB
client = MongoClient(mongo_uri)
db = client[db_name]

# Check for duplicate username
if db.users.find_one({"username": username}):
    print(f"❌ User '{username}' already exists.")
    sys.exit(1)

# Create user document with role 'pwd'
user = {
    "username": username,
    "password_hash": generate_password_hash(password),
    "role": "pwd"  # role stays as 'pwd'
}

res = db.users.insert_one(user)
print(f"✅ Created PWD staff user '{username}' with id: {res.inserted_id}")
