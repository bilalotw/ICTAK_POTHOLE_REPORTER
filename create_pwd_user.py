# Helper script to create a PWD staff account in MongoDB.
# Usage: python create_pwd_user.py username password
import sys
from pymongo import MongoClient
from werkzeug.security import generate_password_hash

if len(sys.argv) < 3:
    print("Usage: python create_pwd_user.py <username> <password>")
    sys.exit(1)

username = sys.argv[1]
password = sys.argv[2]

client = MongoClient("mongodb://localhost:27017/")
db = client.pothole_db

user = {
    "username": username,
    "password_hash": generate_password_hash(password),
    "role": "pwd"
}

res = db.users.insert_one(user)
print("Created PWD user with id:", res.inserted_id)
