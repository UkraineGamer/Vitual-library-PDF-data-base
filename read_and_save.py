from pymongo import MongoClient
from gridfs import GridFS
from dotenv import load_dotenv
from pathlib import Path
import os


class Books_open:
    def __init__(self):
        self.mongo_uri = ""
        self.cluster = ""
        self.client = None
        self.db = None
        self.fs = None
        self.files_collection = None

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
        self.files_collection = self.db["books"]
        return self.db

    def file_gfs_upload(self):
        if self.fs is None or self.files_collection is None:
            self.connect_mongodb()
        assert self.fs is not None and self.files_collection is not None

        file_path = Path(
            input("Будь ласка, вставте сюди назву вашого файлу: ").strip().strip('"')
        )
        if not file_path.exists():
            raise FileNotFoundError(f"Файл не знайдено: {file_path.resolve()}")

        with file_path.open("rb") as f:
            file_id = self.fs.put(f, filename=file_path.name)

        file_saved = {
            "file_id": file_id,
            "filename": file_path.name,
        }
        result = self.files_collection.insert_one(file_saved)
        return result.inserted_id

db = Books_open()
db.connect_mongodb()
db.file_gfs_upload()
