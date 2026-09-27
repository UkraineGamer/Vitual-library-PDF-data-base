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

    def register_user(self, username, password):
        self.cur.execute("""CREATE TABLE IF NOT EXISTS users (id SERIAL PRIMARY KEY, username VARCHAR(100), password VARCHAR(20));""" )

        # Check if the username already exists
        self.cur.execute("SELECT * FROM users WHERE username = %s", (username,))
        existing_user = self.cur.fetchone()

        if existing_user:
            return False  # Username already exists

        # Insert the new user into the database
        self.cur.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
        
        self.conn.commit()
        self.cur.close()
        self.conn.close()
        return True  # Registration successful