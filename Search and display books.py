from pymongo import MongoClient
from gridfs import GridFS
from dotenv import load_dotenv
from pathlib import Path
import os

load_dotenv(Path("secure.env"))

client = os.getenv("MONGO_URI")
db = client["libary"]
collection = db["books"]

def display_books():
    print("Список книг:\n")
    for book in collection.find():
        print(book["title"], book["author"], book["year"])

def search_books(title):
    search = input("\n Введіть назву книги: ")
    result = collection.find_one({title: [search]})

    if result:
        print(f"Знайдена книга: {result['title']} автор: {result['author']} рік видання: {result['year']}")
    else:
        print("книгу не знайдено")

display_books()

book_title = input("\n Введіть назву книги для рошуку: ")
search_books(book_title)
