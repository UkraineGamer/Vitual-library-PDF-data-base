import os

import bcrypt
from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from pymongo.server_api import ServerApi


class UserRegister:
    def __init__(self):
        load_dotenv()
        uri = self._required_env('MONGO_URI')
        database = self._required_env('MONGO_USERS_DB_NAME')
        collection = os.getenv('MONGO_ACCOUNTS_COLLECTION_NAME') or self._required_env('MONGO_ACCAUNTS_COLLECTION_NAME')
        self.client = MongoClient(uri, server_api=ServerApi('1'), serverSelectionTimeoutMS=8000)
        try:
            self.client.admin.command('ping')
            self.mongo_collection = self.client[database][collection]
            self.mongo_collection.create_index('username', unique=True)
        except Exception:
            self.client.close()
            raise

    @staticmethod
    def _required_env(name: str) -> str:
        value = os.getenv(name)
        if not value or not value.strip():
            raise RuntimeError(f'Missing required environment variable: {name}')
        return value.strip()

    @staticmethod
    def _credentials(username: str, password: str) -> tuple[str, bytes]:
        if not isinstance(username, str) or not isinstance(password, str):
            raise ValueError('Username and password must be text.')
        username = username.strip()
        encoded = password.encode('utf-8')
        if not username or not encoded or len(encoded) > 72:
            raise ValueError('Enter a username and a password of 1 to 72 UTF-8 bytes.')
        return username, encoded

    def register_user(self, username: str, password: str) -> bool:
        username, encoded = self._credentials(username, password)
        if self.mongo_collection.find_one({'username': username}) is not None:
            return False
        user = {'username': username, 'password': bcrypt.hashpw(encoded, bcrypt.gensalt()).decode('utf-8')}
        try:
            self.mongo_collection.insert_one(user)
        except DuplicateKeyError:
            return False
        return True

    def login_user(self, username: str, password: str) -> bool:
        try:
            username, encoded = self._credentials(username, password)
        except ValueError:
            return False
        user = self.mongo_collection.find_one({'username': username})
        if user is None:
            return False
        hashed = user.get('password')
        if isinstance(hashed, str):
            hashed = hashed.encode('utf-8')
        if not isinstance(hashed, bytes):
            return False
        try:
            return bcrypt.checkpw(encoded, hashed)
        except ValueError:
            return False

    def close(self):
        self.client.close()
