from fileinput import filename
from pymongo import MongoClient
from gridfs import GridFS
from dotenv import load_dotenv
from pathlib import Path
import os

from pymongo.synchronous import collection

class Books_open:
    def __init__(self):
        self.mongo_uri = ""
        self.cluster = ""
        self.client = None
        self.db = None
        self.fs = None

    def get_uri(self):
        load_dotenv(Path("secure.env"))
        self.mongo_uri = os.getenv("MONGO_URI")
        self.cluster = os.getenv("appName")

    def connect_mongodb(self, db_name: str | None = None):
        self.get_uri()
        if not self.mongo_uri:
            raise ValueError("MONGO_URI is not set in secure.env")

        self.client = MongoClient(self.mongo_uri)
        self.client.admin.command("ping")

        db_name = db_name or os.getenv("MONGO_DB", "library")
        self.db = self.client[db_name]
        self.fs = GridFS(self.db)
        return self.db

    def file_gfs_upload(self):
        fs = self.fs
        file_directory = str(input("Будь ласка, вставте сюди назву вашого файлу: "))
        name = file_directory.split(".")[0]
        with open(f"{name}.pdf", "rb") as f:
            file_id = fs.put(
                f,
                filename=f"{name}.pdf"
            )
        file_saved = {
            id: file_id,
            name: f"{name}.pdf"
        }
        collection.insert_one(file_saved)    
