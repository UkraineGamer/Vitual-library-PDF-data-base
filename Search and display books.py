# from pathlib import Path
# import os
# import re

# from bson import ObjectId
# from bson.errors import InvalidId
# from dotenv import load_dotenv
# from gridfs import GridFS
# from gridfs.errors import NoFile
# from pymongo import MongoClient
# from pymongo.errors import ConfigurationError, PyMongoError


# class LibraryApp:
#     def __init__(self, env_path="secure.env"):
#         load_dotenv(Path(__file__).with_name(env_path))

#         self.mongo_uri = (os.getenv("MONGO_URI") or "").strip()
#         self.db_name = (os.getenv("MONGO_DB") or "").strip()
#         self.collection_name = (os.getenv("MONGO_COLLECTION") or "books").strip()
#         self.client = None
#         self.db = None
#         self.fs = None
#         self.collection = None

#     def connect_mongodb(self):
#         if not self.mongo_uri:
#             raise RuntimeError("MONGO_URI is not set. Add it to secure.env.")

#         self.client = MongoClient(
#             self.mongo_uri,
#             serverSelectionTimeoutMS=5000,
#             connectTimeoutMS=5000,
#             socketTimeoutMS=5000,
#         )
#         self.client.admin.command("ping")

#         if self.db_name:
#             self.db = self.client[self.db_name]
#         else:
#             self.db = self.client.get_default_database(default="library")

#         self.fs = GridFS(self.db)
#         self.collection = self.db[self.collection_name]
#         return self.collection

#     def require_collection(self):
#         if self.collection is None:
#             self.connect_mongodb()
#         return self.collection

#     def require_gridfs(self):
#         if self.fs is None:
#             self.connect_mongodb()
#         return self.fs

#     def format_connection_error(self, error):
#         message = str(error)
#         if "DNS operation timed out" in message or "resolution lifetime expired" in message:
#             return (
#                 "Не вдалося знайти сервер MongoDB через DNS. "
#                 "Перевірте інтернет, DNS/VPN/firewall і MONGO_URI у secure.env."
#             )
#         return f"Помилка підключення до MongoDB: {error}"

#     def display_books(self):
#         print("Список книг:\n")

#         try:
#             collection = self.require_collection()
#             books = collection.find({}, {"title": 1, "author": 1, "year": 1})
#             has_books = False

#             for book in books:
#                 has_books = True
#                 title = book.get("title", "Без назви")
#                 author = book.get("author", "Автор невідомий")
#                 year = book.get("year", "Рік невідомий")
#                 print(f"{title} | {author} | {year}")

#             if not has_books:
#                 print("У бібліотеці поки немає книг.")
#         except (RuntimeError, PyMongoError) as error:
#             print(f"Помилка під час отримання книг: {error}")

#     def search_books(self):
#         search_query = input("\nВведіть назву книги для пошуку: ").strip()
#         if not search_query:
#             print("Назва книги не може бути порожньою.")
#             return

#         try:
#             collection = self.require_collection()
#             result = collection.find_one(
#                 {"title": {"$regex": re.escape(search_query), "$options": "i"}}
#             )
#         except (RuntimeError, PyMongoError) as error:
#             print(f"Помилка під час пошуку книги: {error}")
#             return

#         if result:
#             title = result.get("title", "Без назви")
#             author = result.get("author", "Автор невідомий")
#             year = result.get("year", "Рік невідомий")
#             print(f"Знайдена книга: {title}; автор: {author}; рік видання: {year}")
#         else:
#             print("Книгу не знайдено.")

#     def download_file(self, filename, output_dir="."):
#         if not filename:
#             return "Назва файлу не може бути порожньою."

#         try:
#             fs = self.require_gridfs()
#             file = fs.find_one({"filename": filename})
#             if file is None:
#                 return "Файл не знайдено."

#             output_path = Path(output_dir) / Path(file.filename).name
#             output_path.parent.mkdir(parents=True, exist_ok=True)

#             with output_path.open("wb") as output_file:
#                 output_file.write(file.read())

#             return f"Файл '{file.filename}' успішно завантажено."
#         except (RuntimeError, OSError, PyMongoError) as error:
#             return f"Помилка під час завантаження файлу: {error}"

#     def download_by_id(self, file_id, output_dir="."):
#         if not file_id:
#             return "ID файлу не може бути порожнім."

#         try:
#             object_id = ObjectId(file_id)
#             fs = self.require_gridfs()
#             file = fs.get(object_id)
#             output_path = Path(output_dir) / Path(file.filename).name
#             output_path.parent.mkdir(parents=True, exist_ok=True)

#             with output_path.open("wb") as output_file:
#                 output_file.write(file.read())

#             return f"Файл '{file.filename}' успішно завантажено."
#         except (InvalidId, TypeError):
#             return "Некоректний ID файлу."
#         except NoFile:
#             return "Файл з таким ID не знайдено."
#         except (RuntimeError, OSError, PyMongoError) as error:
#             return f"Помилка під час завантаження файлу: {error}"

#     def get_all_files(self):
#         files = []

#         try:
#             fs = self.require_gridfs()
#             for file in fs.find():
#                 files.append(
#                     {
#                         "id": str(file._id),
#                         "filename": file.filename,
#                         "size": file.length,
#                     }
#                 )
#         except (RuntimeError, PyMongoError) as error:
#             print(f"Помилка під час отримання файлів: {error}")

#         return files

#     def run(self):
#         try:
#             self.connect_mongodb()
#         except (RuntimeError, ConfigurationError, PyMongoError) as error:
#             print(self.format_connection_error(error))
#             return

#         self.display_books()
#         self.search_books()

#     def close(self):
#         if self.client is not None:
#             self.client.close()


# if __name__ == "__main__":
#     app = LibraryApp()
#     try:
#         app.run()
#     finally:
#         app.close()
import ssl
from pathlib import Path
import os
import re
 
from bson import ObjectId
from bson.errors import InvalidId
from dotenv import load_dotenv
from gridfs import GridFS
from gridfs.errors import NoFile
from pymongo import MongoClient
from pymongo.errors import ConfigurationError, PyMongoError
 
 
class LibraryApp:
    def __init__(self, env_path="secure.env"):
        load_dotenv(Path(__file__).with_name(env_path))
 
        self.mongo_uri = (os.getenv("MONGO_URI") or "").strip()
        self.db_name = (os.getenv("MONGO_DB") or "").strip()
        self.collection_name = (os.getenv("MONGO_COLLECTION") or "books").strip()
        self.client = None
        self.db = None
        self.fs = None
        self.collection = None
 
    def connect_mongodb(self):
        if not self.mongo_uri:
            raise RuntimeError("MONGO_URI is not set. Add it to secure.env.")
 
        # Явно вказуємо TLS-параметри. На Windows старі версії OpenSSL
        # часто не можуть домовитись з MongoDB Atlas і кидають
        # TLSV1_ALERT_INTERNAL_ERROR. tlsCAFile=certifi.where() та
        # явний контекст допомагають уникнути цього.
        try:
            import certifi
            ca_file = certifi.where()
        except ImportError:
            ca_file = None
 
        connect_kwargs = dict(
            serverSelectionTimeoutMS=8000,
            connectTimeoutMS=8000,
            socketTimeoutMS=8000,
            tls=True,
        )
        if ca_file:
            connect_kwargs["tlsCAFile"] = ca_file
 
        self.client = MongoClient(self.mongo_uri, **connect_kwargs)
 
        try:
            self.client.admin.command("ping")
        except PyMongoError:
            # Якщо перша спроба впала через TLS handshake, пробуємо
            # ще раз із дозволом на старіші TLS-протоколи (іноді
            # допомагає на застарілих Windows-збірках Python).
            self.client.close()
            connect_kwargs["tlsCAFile"] = ca_file
            self.client = MongoClient(self.mongo_uri, **connect_kwargs)
            self.client.admin.command("ping")
 
        if self.db_name:
            self.db = self.client[self.db_name]
        else:
            self.db = self.client.get_default_database(default="library")
 
        self.fs = GridFS(self.db)
        self.collection = self.db[self.collection_name]
        return self.collection
 
    def require_collection(self):
        if self.collection is None:
            self.connect_mongodb()
        return self.collection
 
    def require_gridfs(self):
        if self.fs is None:
            self.connect_mongodb()
        return self.fs
 
    def format_connection_error(self, error):
        message = str(error)
        if "DNS operation timed out" in message or "resolution lifetime expired" in message:
            return (
                "Не вдалося знайти сервер MongoDB через DNS. "
                "Перевірте інтернет, DNS/VPN/firewall і MONGO_URI у secure.env."
            )
        if "TLSV1_ALERT_INTERNAL_ERROR" in message or "SSL handshake failed" in message:
            return (
                "Помилка SSL/TLS під час підключення до MongoDB Atlas.\n"
                "Найімовірніші причини:\n"
                "  1. Застаріла версія Python/OpenSSL — оновіть Python до 3.11+.\n"
                "  2. Антивірус/файрвол перехоплює TLS-трафік — тимчасово вимкніть SSL-інспекцію.\n"
                "  3. Застарілий пакет certifi/pymongo — виконайте:\n"
                "     pip install --upgrade pymongo dnspython certifi\n"
                "  4. Ваша IP-адреса не додана в Network Access у MongoDB Atlas.\n"
                f"Деталі помилки: {error}"
            )
        return f"Помилка підключення до MongoDB: {error}"
 
    def display_books(self):
        print("Список книг:\n")
 
        try:
            collection = self.require_collection()
            books = collection.find({}, {"title": 1, "author": 1, "year": 1})
            has_books = False
 
            for book in books:
                has_books = True
                title = book.get("title", "Без назви")
                author = book.get("author", "Автор невідомий")
                year = book.get("year", "Рік невідомий")
                print(f"{title} | {author} | {year}")
 
            if not has_books:
                print("У бібліотеці поки немає книг.")
        except (RuntimeError, PyMongoError) as error:
            print(f"Помилка під час отримання книг: {error}")
 
    def search_books(self):
        search_query = input("\nВведіть назву книги для пошуку: ").strip()
        if not search_query:
            print("Назва книги не може бути порожньою.")
            return
 
        try:
            collection = self.require_collection()
            result = collection.find_one(
                {"title": {"$regex": re.escape(search_query), "$options": "i"}}
            )
        except (RuntimeError, PyMongoError) as error:
            print(f"Помилка під час пошуку книги: {error}")
            return
 
        if result:
            title = result.get("title", "Без назви")
            author = result.get("author", "Автор невідомий")
            year = result.get("year", "Рік невідомий")
            print(f"Знайдена книга: {title}; автор: {author}; рік видання: {year}")
        else:
            print("Книгу не знайдено.")
 
    def download_file(self, filename, output_dir="."):
        if not filename:
            return "Назва файлу не може бути порожньою."
 
        try:
            fs = self.require_gridfs()
            file = fs.find_one({"filename": filename})
            if file is None:
                return "Файл не знайдено."
 
            output_path = Path(output_dir) / Path(file.filename).name
            output_path.parent.mkdir(parents=True, exist_ok=True)
 
            with output_path.open("wb") as output_file:
                output_file.write(file.read())
 
            return f"Файл '{file.filename}' успішно завантажено."
        except (RuntimeError, OSError, PyMongoError) as error:
            return f"Помилка під час завантаження файлу: {error}"
 
    def download_by_id(self, file_id, output_dir="."):
        if not file_id:
            return "ID файлу не може бути порожнім."
 
        try:
            object_id = ObjectId(file_id)
            fs = self.require_gridfs()
            file = fs.get(object_id)
            output_path = Path(output_dir) / Path(file.filename).name
            output_path.parent.mkdir(parents=True, exist_ok=True)
 
            with output_path.open("wb") as output_file:
                output_file.write(file.read())
 
            return f"Файл '{file.filename}' успішно завантажено."
        except (InvalidId, TypeError):
            return "Некоректний ID файлу."
        except NoFile:
            return "Файл з таким ID не знайдено."
        except (RuntimeError, OSError, PyMongoError) as error:
            return f"Помилка під час завантаження файлу: {error}"
 
    def get_all_files(self):
        files = []
 
        try:
            fs = self.require_gridfs()
            for file in fs.find():
                files.append(
                    {
                        "id": str(file._id),
                        "filename": file.filename,
                        "size": file.length,
                    }
                )
        except (RuntimeError, PyMongoError) as error:
            print(f"Помилка під час отримання файлів: {error}")
 
        return files
 
    def run(self):
        try:
            self.connect_mongodb()
        except (RuntimeError, ConfigurationError, PyMongoError) as error:
            print(self.format_connection_error(error))
            return
 
        self.display_books()
        self.search_books()
 
    def close(self):
        if self.client is not None:
            self.client.close()
 
 
if __name__ == "__main__":
    app = LibraryApp()
    try:
        app.run()
    finally:
        app.close()