from pathlib import Path
import os
import re

from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.errors import PyMongoError


load_dotenv(Path(__file__).with_name("secure.env"))

DATABASE_NAME = os.getenv("MONGO_DB", "library")
COLLECTION_NAME = os.getenv("MONGO_COLLECTION", "books")


def get_books_collection():
    mongo_uri = os.getenv("MONGO_URI")
    if not mongo_uri:
        raise RuntimeError("MONGO_URI is not set. Add it to secure.env.")

    client = MongoClient(mongo_uri)
    return client[DATABASE_NAME][COLLECTION_NAME]


def display_books(collection):
    print("Список книг:\n")

    try:
        books = collection.find({}, {"title": 1, "author": 1, "year": 1})
    except PyMongoError as error:
        print(f"Помилка під час отримання книг: {error}")
        return

    has_books = False
    for book in books:
        has_books = True
        title = book.get("title", "Без назви")
        author = book.get("author", "Автор невідомий")
        year = book.get("year", "Рік невідомий")
        print(f"{title} | {author} | {year}")

    if not has_books:
        print("У бібліотеці поки немає книг.")


def search_books(collection):
    search_query = input("\nВведіть назву книги для пошуку: ").strip()
    if not search_query:
        print("Назва книги не може бути порожньою.")
        return

    try:
        result = collection.find_one(
            {"title": {"$regex": re.escape(search_query), "$options": "i"}}
        )
    except PyMongoError as error:
        print(f"Помилка під час пошуку книги: {error}")
        return

    if result:
        title = result.get("title", "Без назви")
        author = result.get("author", "Автор невідомий")
        year = result.get("year", "Рік невідомий")
        print(f"Знайдена книга: {title}; автор: {author}; рік видання: {year}")
    else:
        print("Книгу не знайдено.")


def main():
    try:
        collection = get_books_collection()
    except RuntimeError as error:
        print(error)
        return

    display_books(collection)
    search_books(collection)


if __name__ == "__main__":
    main()
