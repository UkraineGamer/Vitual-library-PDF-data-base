import os
from dotenv import load_dotenv

class Setup:
    def __init__(self):
        load_dotenv()
        self.mongo_uri = os.getenv("MONGO_URI")
        self.mongo_db_name = os.getenv("MONGO_DB_NAME")
        self.mongo_cluster_name = os.getenv("MONGO_CLUSTER_NAME")
        self.mongo_collection_name = os.getenv("MONGO_COLLECTION_NAME")

    def get_mongo_uri(self):
        return self.mongo_uri

    def get_mongo_db_name(self):
        return self.mongo_db_name

    def get_mongo_cluster_name(self):
        return self.mongo_cluster_name

    def get_mongo_collection_name(self):
        return self.mongo_collection_name

    def initialize_setup(self):
        self.get_mongo_uri()
        self.get_mongo_db_name()
        self.get_mongo_cluster_name()
        self.get_mongo_collection_name()
        return self.mongo_uri, self.mongo_db_name, self.mongo_cluster_name, self.mongo_collection_name