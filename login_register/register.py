import os
from dotenv import load_dotenv
import os
from pymongo import MongoClient
from pymongo.server_api import ServerApi
import bcrypt

class UserRegister:
    def __init__(self):
        load_dotenv()
        self.mongo_uri = self._required_env("MONGO_URI")
        self.client = MongoClient(self.mongo_uri, server_api=ServerApi('1'))

        try:
            self.client.admin.command('ping')
            print("Pinged your deployment. You successfully connected to MongoDB!")
        except Exception as exc:
            raise ConnectionError(
                "Could not authenticate with MongoDB Atlas. Check MONGO_URI, "
                "the Atlas database user, and Network Access settings."
            ) from exc

        self.mongo_db = self._required_env("MONGO_USERS_DB_NAME")
        collection_name = self._required_env("MONGO_ACCAUNTS_COLLECTION_NAME")
        self.mongo_collection = self.client[self.mongo_db][collection_name]

    @staticmethod
    def _required_env(name: str) -> str:
        value = os.getenv(name)
        if not value:
            raise RuntimeError(f"Missing required environment variable: {name}")
        return value

    def register_user(self, username: str, password: str):
        existing_user = self.mongo_collection.find_one({"username": username})
        if existing_user:
            return f"User '{username}' already exists."

        user_data = {
            "username": username,
            "password": bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        }

        self.mongo_collection.insert_one(user_data)
        return f"User '{username}' registered successfully."