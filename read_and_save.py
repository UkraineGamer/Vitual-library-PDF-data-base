from pymongo import MongoClient
from gridfs import GridFS
from dotenv import load_dotenv
import os

class Books_open:
    def __init__(self):
        load_dotenv()
        self.mongo_uri = os.getenv("secure")
        self.client = MongoClient()

    def file_gfs_upload(self, file_pdf):
        