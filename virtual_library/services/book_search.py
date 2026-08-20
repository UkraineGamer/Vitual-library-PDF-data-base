from tkinter import filedialog
from urllib.parse import quote

import requests


class BookSearch:
    """Search Open Library and let the user choose a local book file."""

    def __init__(self) -> None:
        self.file_root = ""

    def search_books(self, title: str) -> list[dict]:
        try:
            response = requests.get(
                f"https://openlibrary.org/search.json?title={quote(title)}", timeout=10
            )
            response.raise_for_status()
        except requests.RequestException:
            return []

        results: list[dict] = []
        for index, book in enumerate(response.json().get("docs", [])[:10]):
            year = book.get("first_publish_year", "Невідомо")
            isbn_list = book.get("isbn", [])
            results.append(
                {
                    "id": book.get("key", f"ol-{index}").replace("/works/", "ol-"),
                    "title": book.get("title", "Невідомо"),
                    "author": ", ".join(book.get("author_name", ["Невідомо"])),
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
        return results

    def get_file_path(self, parent=None) -> str:
        file_path = filedialog.askopenfilename(parent=parent)
        self.file_root = str(file_path) if file_path else ""
        return self.file_root
