from pymongo import MongoClient
from pymongo.server_api import ServerApi
from gridfs import GridFS
from gridfs.errors import NoFile
from bson import ObjectId
from dotenv import load_dotenv
from pathlib import Path, PureWindowsPath
from shutil import copyfileobj
import os
import re

class Books_download:
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

    def download_file_gfs(self, file_id: str | ObjectId, output_path: str | Path):
        if isinstance(file_id, str):
            if not ObjectId.is_valid(file_id):
                raise ValueError(
                    "file_id must be a 24-character hexadecimal MongoDB ObjectId."
                )
            file_id = ObjectId(file_id)

        output_folder = Path(output_path)
        output_folder.mkdir(parents=True, exist_ok=True)

        try:
            file_data = self.fs.get(file_id)
        except NoFile as exc:
            raise FileNotFoundError(
                f"No GridFS file exists with ID: {file_id}"
            ) from exc
        with file_data:
            filename = file_data.filename
            if (not isinstance(filename, str) or not filename or filename in (".", "..")
                    or Path(filename).name != filename or PureWindowsPath(filename).name != filename
                    or ":" in filename):
                raise ValueError("GridFS filename must be a plain filename.")
            output_file_path = output_folder / filename
            # Exclusive creation preserves existing files, including symlinks.
            with output_file_path.open("xb") as output:
                try:
                    copyfileobj(file_data, output)
                except Exception:
                    output.close()
                    output_file_path.unlink()
                    raise
        return output_file_path
