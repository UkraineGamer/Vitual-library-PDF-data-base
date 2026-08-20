import os
from dataclasses import dataclass

from dotenv import load_dotenv


@dataclass(frozen=True)
class Settings:
    mongo_uri: str | None
    mongo_db_name: str | None
    mongo_cluster_name: str | None
    mongo_collection_name: str | None


def load_settings() -> Settings:
    load_dotenv()
    return Settings(
        mongo_uri=os.getenv("MONGO_URI"),
        mongo_db_name=os.getenv("MONGO_DB_NAME"),
        mongo_cluster_name=os.getenv("MONGO_CLUSTER_NAME"),
        mongo_collection_name=os.getenv("MONGO_COLLECTION_NAME"),
    )
