from pymongo import MongoClient
from gridfs import GridFS
from dotenv import load_dotenv
import os

db = client["libary"]
collection = db["books"]

print("Список книг:/n")

