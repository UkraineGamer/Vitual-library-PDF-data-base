"""Compatibility entry point for uploading a PDF using the current storage service."""
from pathlib import Path

from file_download_upload_parse.upload import Books_upload


class Books_open:
    def __init__(self):
        self.uploader = None

    def connect_mongodb(self, db_name: str | None = None):
        if self.uploader is None:
            self.uploader = Books_upload()
        if db_name and db_name != self.uploader.mongo_db:
            raise ValueError("Set MONGO_DB_NAME in .env to select the database.")
        return self.uploader.client[self.uploader.mongo_db]

    def file_gfs_upload(self, file_path=None):
        if file_path is None:
            file_path = input("PDF file path: ").strip().strip('"')
        if not file_path:
            raise ValueError("A PDF file path is required.")
        self.connect_mongodb()
        return self.uploader.upload_file_gfs(Path(file_path))

    def close(self):
        if self.uploader is not None:
            self.uploader.client.close()


if __name__ == "__main__":
    app = Books_open()
    try:
        print(app.file_gfs_upload())
    finally:
        app.close()
