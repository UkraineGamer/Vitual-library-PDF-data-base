from pymongo import MongoClient
from pymongo.server_api import ServerApi
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
        self.client = MongoClient(self.mongo_uri, server_api=ServerApi('1'))

        try:
            self.client.admin.command('ping')
            print("Pinged your deployment. You successfully connected to MongoDB!")
        except Exception as exc:
            raise ConnectionError(
                "Could not authenticate with MongoDB Atlas. Check MONGO_URI, "
                "the Atlas database user, and Network Access settings."
            ) from exc

        self.mongo_db = self._required_env("MONGO_DB_NAME")
        collection_name = self._required_env("MONGO_COLLECTION_NAME")
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

    def file_exists(self, file_id: str | Path):
        return self.mongo_collection.find_one({"file_id": file_id}) is not None
    
    def upload_file_gfs(self, file_path: str | Path):
        if self.file_exists(file_path):
            raise FileExistsError(f"File '{file_path}' already exists in the database.\nSkipping upload.")
            return None
        else:
            file_path = Path(file_path)

            with file_path.open("rb") as f:
                file_id = self.fs.put(f, filename=file_path.name)
        
            file_saved = {
                "file_id": file_id,
                "filename": file_path.name,
                }
            result = self.mongo_collection.insert_one(file_saved)
            print(f"File '{file_path.name}' uploaded to GridFS with ID: {file_id}")
            return result.inserted_id
    
# if __name__ == "__main__":
#     open_books = Books_upload()
#     open_books.upload_file_gfs(Path(__file__).resolve().parents[1] / "testing.pdf")