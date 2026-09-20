from pymongo import MongoClient
from pymongo.server_api import ServerApi
from pymongo.errors import DuplicateKeyError
from gridfs import GridFS
from dotenv import load_dotenv
from pathlib import Path
import os
import re

class Books_upload:
    def __init__(self):
        load_dotenv()
        self.mongo_uri = self._normalise_mongo_uri(
            self._required_env("MONGO_URI")
        )
        self.mongo_db = self._required_env("MONGO_DB_NAME")
        collection_name = self._required_env("MONGO_COLLECTION_NAME")
        self.client = MongoClient(self.mongo_uri, server_api=ServerApi('1'), serverSelectionTimeoutMS=8000)

        try:
            self.client.admin.command('ping')
            print("Pinged your deployment. You successfully connected to MongoDB!")
        except Exception as exc:
            self.client.close()
            raise ConnectionError(
                "Could not authenticate with MongoDB Atlas. Check MONGO_URI, "
                "the Atlas database user, and Network Access settings."
            ) from exc

        self.fs = GridFS(self.client[self.mongo_db])
        self.mongo_collection = self.client[self.mongo_db][collection_name]

    @staticmethod
    def _required_env(name: str) -> str:
        value = os.getenv(name)
        if not value:
            raise RuntimeError(f"Missing required environment variable: {name}")
        return value

    @staticmethod
    def _normalise_mongo_uri(uri: str) -> str:
        """Remove Atlas UI's optional <password> placeholder brackets."""
        return re.sub(r":<([^>]*)>@", r":\1@", uri)

    def file_exists(self, file_path: str | Path) -> bool:
        return self.mongo_collection.find_one({"filename": Path(file_path).name}) is not None

    def upload_file_gfs(self, file_path: str | Path):
        file_path = Path(file_path)
        if not file_path.is_file():
            raise FileNotFoundError(file_path)
        with file_path.open("rb") as source:
            if file_path.suffix.lower() != ".pdf" or source.read(5) != b"%PDF-":
                raise ValueError("Choose a PDF file with a valid PDF header.")
            source.seek(0)
            # The unique index also protects simultaneous uploads of the same name.
            self.mongo_collection.create_index("filename", unique=True, partialFilterExpression={"filename": {"$type": "string"}})
            if self.file_exists(file_path):
                raise FileExistsError(f"File '{file_path.name}' already exists.")
            file_id = self.fs.put(source, filename=file_path.name)
        try:
            self.mongo_collection.insert_one({"file_id": file_id, "filename": file_path.name})
        except Exception as error:
            self.fs.delete(file_id)
            if isinstance(error, DuplicateKeyError):
                raise FileExistsError(f"File '{file_path.name}' already exists.") from error
            raise
        return file_id
