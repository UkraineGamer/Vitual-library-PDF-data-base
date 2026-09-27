"""Command-line catalogue search and GridFS downloads."""
import os
import re
from pathlib import Path

from bson import ObjectId
from dotenv import load_dotenv
from gridfs import GridFS
from pymongo import MongoClient
from pymongo.errors import PyMongoError

from file_download_upload_parse.download import Books_download


class LibraryApp:
    def __init__(self, env_path=".env"):
        load_dotenv(Path(__file__).with_name(env_path))
        self.mongo_uri = (os.getenv("MONGO_URI") or "").strip()
        self.db_name = os.getenv("MONGO_DB_NAME") or os.getenv("MONGO_DB") or "library"
        self.collection_name = os.getenv("MONGO_COLLECTION_NAME") or os.getenv("MONGO_COLLECTION") or "books"
        self.client = self.db = self.fs = self.collection = None

    def connect_mongodb(self):
        if not self.mongo_uri:
            raise RuntimeError("Set MONGO_URI in your local .env file.")
        self.close()
        self.client = MongoClient(Books_download._normalise_mongo_uri(self.mongo_uri), serverSelectionTimeoutMS=8000)
        try:
            self.client.admin.command("ping")
            self.db = self.client[self.db_name]
            self.fs = GridFS(self.db)
            self.collection = self.db[self.collection_name]
        except Exception:
            self.close()
            raise
        return self.collection

    def require_collection(self):
        if self.collection is None:
            self.connect_mongodb()
        return self.collection

    def require_gridfs(self):
        if self.fs is None:
            self.connect_mongodb()
        return self.fs

    @staticmethod
    def format_connection_error(error):
        if isinstance(error, RuntimeError):
            return str(error)
        return "Cannot connect to MongoDB. Check .env, network access and database permissions."

    def display_books(self):
        books = list(self.require_collection().find({}, {"title": 1, "filename": 1, "author": 1, "year": 1}))
        for book in books:
            print(f"{book.get('title') or book.get('filename', 'Untitled')} | {book.get('author', 'Unknown')} | {book.get('year', 'Unknown')}")
        if not books:
            print("No books found.")
        return books

    def search_books(self, query=None):
        query = input("Book title or filename: ") if query is None else query
        query = query.strip()
        if not query:
            return []
        expression = {"$regex": re.escape(query), "$options": "i"}
        books = list(self.require_collection().find({"$or": [{"title": expression}, {"filename": expression}]}))
        for book in books:
            print(book.get('title') or book.get('filename', 'Untitled'))
        if not books:
            print("No matching books.")
        return books

    def download_by_id(self, file_id, output_dir="."):
        if not isinstance(file_id, (str, ObjectId)) or not ObjectId.is_valid(file_id):
            return "Invalid file ID."
        try:
            self.require_gridfs()
            path = Books_download.download_file_gfs(self, file_id, output_dir)
            return f"Downloaded: {path}"
        except (ValueError, RuntimeError, OSError, PyMongoError) as error:
            return f"Download failed: {error}"

    def download_file(self, filename, output_dir="."):
        if not filename:
            return "A filename is required."
        try:
            file = self.require_gridfs().find_one({"filename": filename})
            if file is None:
                return "File not found."
            return self.download_by_id(file._id, output_dir)
        except (RuntimeError, PyMongoError):
            return "Cannot access the file database."

    def get_all_files(self):
        return [{"id": str(file._id), "filename": file.filename, "size": file.length}
                for file in self.require_gridfs().find()]

    def run(self):
        try:
            self.display_books()
            self.search_books()
        except (RuntimeError, PyMongoError) as error:
            print(self.format_connection_error(error))

    def close(self):
        if self.client is not None:
            self.client.close()
        self.client = self.db = self.fs = self.collection = None


if __name__ == "__main__":
    app = LibraryApp()
    try:
        app.run()
    finally:
        app.close()
