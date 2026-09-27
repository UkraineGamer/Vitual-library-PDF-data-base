import psycopg2
import os
from dotenv import load_dotenv

class Register:
    def __init__(self):
        load_dotenv()

        self.conn = psycopg2.connect(
            host=os.getenv("POSTGRES_HOST"),
            port=os.getenv("POSTGRES_PORT"),
            dbname=os.getenv("POSTGRES_DB"),
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD")
        )

        self.cur = self.conn.cursor()