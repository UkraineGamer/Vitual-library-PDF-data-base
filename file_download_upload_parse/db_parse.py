from pymongo import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
from pathlib import Path
import os
import re

class BookDB_parse:
    def __init__(self):
        load_dotenv()
        self.mongo_uri = self._normalise_mongo_uri(self._required_env("MONGO_URI"))
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

    def for_mass_upload(self, pdf_folder: str | Path):
        folder = Path(pdf_folder)
        if not folder.is_dir():
            raise NotADirectoryError(folder)
        existing_filenames = {doc.get("filename") for doc in self.mongo_collection.find({}, {"filename": 1, "_id": 0})}
        return [path.name for path in sorted(folder.iterdir())
                if path.is_file() and path.suffix.lower() == ".pdf" and path.name not in existing_filenames]
