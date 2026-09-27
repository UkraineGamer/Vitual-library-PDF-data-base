from tkinter import filedialog
from urllib.parse import quote

import requests


class BookSearch:
    """Search Open Library and let the user choose a local book file."""

    def __init__(self) -> None:
        self.file_root = ""

    def search_books(self, title: str) -> list[dict]:
        if not title.strip():
            return []
        try:
            response = requests.get(
                f"https://openlibrary.org/search.json?title={quote(title)}", timeout=10
            )
            response.raise_for_status()
            data = response.json()
        except (requests.RequestException, ValueError):
            return []

        docs = data.get("docs") if isinstance(data, dict) else None
        if not isinstance(docs, list):
            return []
        results: list[dict] = []
        seen = set()
        for index, book in enumerate(docs):
            if not isinstance(book, dict):
                continue
            book_id = str(book.get("key") or f"ol-{index}").replace("/works/", "ol-")
            if book_id in seen:
                continue
            seen.add(book_id)
            year = book.get("first_publish_year", "Невідомо")
            isbn_list = book.get("isbn") or []
            if not isinstance(isbn_list, list):
                isbn_list = []
            authors = book.get("author_name") or ["Невідомо"]
            if not isinstance(authors, list):
                authors = [authors]
            results.append(
                {
                    "id": book_id,
                    "title": str(book.get("title") or "Невідомо"),
                    "author": ", ".join(str(author) for author in authors if author is not None),
                    "meta": f"Рік: {year}",
                    "categories": ["Усі"],
                    "pages": book.get("number_of_pages_median", "—"),
                    "isbn": isbn_list[0] if isbn_list else "—",
                    "format": "—",
                    "size": "—",
                    "rating": "—",
                    "reviews": "0",
                    "language": "—",
                    "date": str(year),
                    "publisher": "—",
                    "description": "Опис недоступний для цього результату пошуку.",
                    "cover_bg": "#151312",
                    "cover_accent": "#c89745",
                }
            )
            if len(results) == 10:
                break
        return results

    def get_file_path(self, parent=None) -> str:
        file_path = filedialog.askopenfilename(parent=parent)
        self.file_root = str(file_path) if file_path else ""
        return self.file_root
