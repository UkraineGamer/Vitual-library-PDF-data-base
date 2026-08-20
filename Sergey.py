import tkinter as tk
from tkinter import font as tkfont
import requests
from tkinter import filedialog
from urllib.parse import quote


COLORS = {
    "app": "#07121f",
    "sidebar": "#0a1624",
    "sidebar_active": "#132742",
    "panel": "#0f1a28",
    "panel_alt": "#132234",
    "panel_soft": "#17283d",
    "input_bg": "#0b1624",
    "input_line": "#1c3046",
    "line": "#203246",
    "line_soft": "#172638",
    "text": "#e8eef8",
    "text_soft": "#a8b4c6",
    "text_muted": "#748195",
    "blue": "#0a84ff",
    "blue_dark": "#086ed3",
    "green": "#35c46a",
    "yellow": "#ffcc33",
    "danger": "#e76f6f",
}

DARK_COLORS = COLORS.copy()
LIGHT_COLORS = {
    "app": "#f4f7fb",
    "sidebar": "#eef3f8",
    "sidebar_active": "#dbeafe",
    "panel": "#ffffff",
    "panel_alt": "#f1f5f9",
    "panel_soft": "#e5edf7",
    "input_bg": "#ffffff",
    "input_line": "#cbd5e1",
    "line": "#c7d2df",
    "line_soft": "#dbe3ec",
    "text": "#172033",
    "text_soft": "#435369",
    "text_muted": "#6f7d91",
    "blue": "#0a84ff",
    "blue_dark": "#086ed3",
    "green": "#238b52",
    "yellow": "#c28700",
    "danger": "#d84f4f",
}

UI_STRINGS = {
    "uk": {
        "search": "Пошук",
        "search_placeholder": "Пошук книг за назвою, автором або ISBN...",
        "download_history": "Історія завантажень",
        "view_all_history": "Переглянути всю історію",
        "full_history": "Повна історія завантажень",
        "settings_title": "Налаштування",
        "interface_language": "Мова інтерфейсу",
        "theme": "Тема оформлення",
        "dark_theme": "Темна",
        "light_theme": "Світла",
        "nav_home": "Головна",
        "nav_search": "Пошук книг",
        "nav_downloads": "Завантаження",
        "nav_history": "Історія",
        "nav_library": "Бібліотека",
        "nav_favorites": "Обране",
        "nav_settings": "Налаштування",
    },
    "en": {
        "search": "Search",
        "search_placeholder": "Search books by title, author, or ISBN...",
        "download_history": "Download history",
        "view_all_history": "View full history",
        "full_history": "Full download history",
        "settings_title": "Settings",
        "interface_language": "Interface language",
        "theme": "Theme",
        "dark_theme": "Dark",
        "light_theme": "Light",
        "nav_home": "Home",
        "nav_search": "Book search",
        "nav_downloads": "Downloads",
        "nav_history": "History",
        "nav_library": "Library",
        "nav_favorites": "Favorites",
        "nav_settings": "Settings",
    },
}


class BookSearch:
    def __init__(self):
        self.file_root = ""

    def search_books(self, title: str) -> list[dict]:
        url = f"https://openlibrary.org/search.json?title={quote(title)}"
        response = requests.get(url, timeout=10)

        if response.status_code != 200:
            return []

        books = response.json().get("docs", [])[:10]
        results: list[dict] = []
        for index, book in enumerate(books):
            year = book.get("first_publish_year", "Невідомо")
            isbn_list = book.get("isbn", [])
            isbn = isbn_list[0] if isbn_list else "—"
            book_id = book.get("key", f"ol-{index}").replace("/works/", "ol-")
            results.append(
                {
                    "id": book_id,
                    "title": book.get("title", "Невідомо"),
                    "author": ", ".join(book.get("author_name", ["Невідомо"])),
                    "meta": f"Рік: {year}",
                    "categories": ["Усі"],
                    "pages": book.get("number_of_pages_median", "—"),
                    "isbn": isbn,
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


BOOKS = [
    {
        "id": "cat",
        "title": "Котик :3",
        "author": "Невідомий автор",
        "meta": "Ілюстрація",
        "categories": ["Усі"],
        "pages": 1,
        "isbn": "—",
        "format": "JPG",
        "size": "—",
        "rating": "0",
        "reviews": "0",
        "language": "Українська",
        "date": "—",
        "publisher": "—",
        "description": "Фото котика.",
        "cover_bg": "#191613",
        "cover_accent": "#f2d17b",
        "cover_image": "Кото-подушка.png",
    },
    {
        "id": "1984",
        "title": "1984",
        "author": "Джордж Орвелл",
        "meta": "Фантастика, Антиутопія",
        "categories": ["Усі", "Художня література"],
        "pages": 328,
        "isbn": "978-0-452-28423-4",
        "format": "EPUB",
        "size": "1.2 МБ",
        "rating": "4.3",
        "reviews": "128",
        "language": "Українська",
        "date": "8 червня 1949",
        "publisher": "Secker & Warburg",
        "description": (
            "Класичний роман-антиутопія про тоталітарне майбутнє, "
            "де держава контролює кожен аспект життя людини."
        ),
        "cover_bg": "#271d17",
        "cover_accent": "#e63737",
    },
    {
        "id": "hobbit",
        "title": "Гобіт, або Туди й назад",
        "author": "Дж. Р. Р. Толкін",
        "meta": "Фентезі, Пригоди",
        "categories": ["Усі", "Художня література"],
        "pages": 310,
        "isbn": "978-0-261-10221-4",
        "format": "EPUB",
        "size": "1.6 МБ",
        "rating": "4.8",
        "reviews": "246",
        "language": "Українська",
        "date": "21 вересня 1937",
        "publisher": "George Allen & Unwin",
        "description": (
            "Подорож Більбо Беггінса до Самотньої гори, повна загадок, "
            "небезпек і відкриттів."
        ),
        "cover_bg": "#153b33",
        "cover_accent": "#79d178",
    },
    {
        "id": "sapiens",
        "title": "Sapiens. Людина розумна",
        "author": "Юваль Ной Харарі",
        "meta": "Нон-фікшн, Історія",
        "categories": ["Усі", "Нон-фікшн", "Історія", "Наука"],
        "pages": 512,
        "isbn": "978-617-12-5470-7",
        "format": "EPUB",
        "size": "1.4 МБ",
        "rating": "4.5",
        "reviews": "312",
        "language": "Українська",
        "date": "2011",
        "publisher": "КСД",
        "description": (
            "Коротка історія людства від появи Homo sapiens до сучасних "
            "суспільств, технологій і глобальних ідей."
        ),
        "cover_bg": "#f4e9d4",
        "cover_accent": "#d95d39",
    },
    {
        "id": "think-grow",
        "title": "Думай і багатій",
        "author": "Наполеон Гілл",
        "meta": "Бізнес, Саморозвиток",
        "categories": ["Усі", "Бізнес"],
        "pages": 176,
        "isbn": "978-966-577-355-6",
        "format": "EPUB",
        "size": "1.1 МБ",
        "rating": "4.1",
        "reviews": "97",
        "language": "Українська",
        "date": "1937",
        "publisher": "The Ralston Society",
        "description": (
            "Практичний погляд на цілі, дисципліну та мислення, яке допомагає "
            "рухатись до фінансових результатів."
        ),
        "cover_bg": "#1d1710",
        "cover_accent": "#c9a44a",
    },
    {
        "id": "short-history",
        "title": "Коротка історія майже всього",
        "author": "Білл Брайсон",
        "meta": "Наука, Популярна наука",
        "categories": ["Усі", "Наука", "Нон-фікшн"],
        "pages": 544,
        "isbn": "978-055-299704-1",
        "format": "EPUB",
        "size": "2.7 МБ",
        "rating": "4.4",
        "reviews": "185",
        "language": "Українська",
        "date": "2003",
        "publisher": "Doubleday",
        "description": (
            "Доступна мандрівка крізь головні наукові відкриття: від космосу "
            "до геології, біології та історії цивілізації."
        ),
        "cover_bg": "#151312",
        "cover_accent": "#c89745",
    },
]



DOWNLOADS = [
    {
        "book_id": "1984",
        "status": "Завершено",
        "date": "Сьогодні, 14:32",
        "size": "1.2 МБ",
        "progress": 100,
    },
    {
        "book_id": "sapiens",
        "status": "Завершено",
        "date": "Вчора, 18:45",
        "size": "2.4 МБ",
        "progress": 100,
    },
    {
        "book_id": "think-grow",
        "status": "Завершено",
        "date": "12.05.2024, 09:12",
        "size": "1.1 МБ",
        "progress": 100,
    },
    {
        "book_id": "hobbit",
        "status": "Завантаження...",
        "date": "",
        "size": "721 КБ / 1.6 МБ",
        "progress": 45,
    },
]


SIDEBAR_ITEMS = [
    ("🏠", "Головна"),
    ("🔎", "Пошук книг"),
    ("📥", "Завантаження"),
    ("🕒", "Історія"),
    ("📚", "Бібліотека"),
    ("💖", "Обране"),
    ("⚙️", "Налаштування"),
]


CATEGORIES = [
    "Усі",
    "Художня література",
    "Нон-фікшн",
    "Наука",
    "Бізнес",
    "Історія",
    "Технології",
    "Більше⌄",
]


class BookDownloaderApp:
    def __init__(self) -> None:
        self.book_search = BookSearch()
        self.root = tk.Tk()
        self.root.title("BookDownloader")
        self.root.geometry("1280x850")
        self.root.minsize(1060, 700)
        self.root.configure(bg=COLORS["app"])

        self.canvas = tk.Canvas(
            self.root,
            bg=COLORS["app"],
            highlightthickness=0,
            bd=0,
        )
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.fonts = self._build_fonts()
        self.buttons: list[dict] = []
        self.hover_action: tuple[str, str | None] | None = None
        self.selected_book_id = "1984"
        self.active_nav = "Пошук книг"
        self.active_category = "Усі"
        self.bookmarks: set[str] = {"1984"}
        self.favorites: set[str] = set()
        self.filter_open = False
        self.filter_format = ""
        self.filter_language = ""
        self.filter_rating = ""
        self.description_expanded = False
        self.interface_language = "uk"
        self.theme_mode = "dark"
        self.placeholder_active = True
        self.api_results: list[dict] | None = None
        self.extra_books: dict[str, dict] = {}
        self.results_scroll = 0
        self.results_scroll_bounds: tuple[float, float, float, float, int] | None = None
        self.results_scrollbar_bounds: tuple[float, float, float, float, int, float, float, float] | None = None
        self.category_scroll = 0
        self.category_scroll_bounds: tuple[float, float, float, float, int] | None = None
        self.category_scrollbar_bounds: tuple[float, float, float, float, int, float, float, float] | None = None
        self.scroll_drag: dict | None = None
        self._search_area_bottom = 120
        self._category_container_geom: dict | None = None
        self.download_col_status_w = 110
        self.download_col_date_w = 132
        self.download_col_size_w = 80
        self.download_col_resize_handles: list[dict] = []
        self.download_data_scroll = 0
        self.download_data_scroll_bounds: tuple[float, float, float, float, int] | None = None
        self.download_data_scrollbar_bounds: tuple[float, float, float, float, int, float, float, float] | None = None

        self.search_entry = tk.Entry(
            self.root,
            bd=0,
            relief=tk.FLAT,
            bg=COLORS["input_bg"],
            fg=COLORS["text_muted"],
            insertbackground=COLORS["text"],
            font=self.fonts["body"],
        )
        self.search_entry.insert(0, UI_STRINGS["uk"]["search_placeholder"])
        self.search_entry.bind("<FocusIn>", self._on_entry_focus_in)
        self.search_entry.bind("<FocusOut>", self._on_entry_focus_out)
        self.search_entry.bind("<KeyRelease>", self._on_search_change)
        self.search_entry.bind("<Return>", lambda _event: self._run_search())

        self.canvas.bind("<Configure>", lambda _event: self.draw())
        self.canvas.bind("<Button-1>", self._on_click)
        self.canvas.bind("<B1-Motion>", self._on_drag)
        self.canvas.bind("<ButtonRelease-1>", self._on_release)
        self.canvas.bind("<MouseWheel>", self._on_mousewheel)
        self.canvas.bind("<Button-4>", self._on_mousewheel)
        self.canvas.bind("<Button-5>", self._on_mousewheel)
        self.canvas.bind("<Motion>", self._on_motion)
        self.canvas.bind("<Leave>", self._on_leave)

        self._apply_theme()
        self.draw()
        self.root.mainloop()

    def _build_fonts(self) -> dict[str, tkfont.Font]:
        return {
            "brand": tkfont.Font(family="Segoe UI", size=10, weight="bold"),
            "nav": tkfont.Font(family="Segoe UI", size=10),
            "body": tkfont.Font(family="Segoe UI", size=13),
            "body_small": tkfont.Font(family="Segoe UI", size=10),
            "caption": tkfont.Font(family="Segoe UI", size=8),
            "section": tkfont.Font(family="Segoe UI Semibold", size=11),
            "title": tkfont.Font(family="Segoe UI Semibold", size=13),
            "detail_title": tkfont.Font(family="Segoe UI Semibold", size=22),
            "button": tkfont.Font(family="Segoe UI Semibold", size=10),
            "cover": tkfont.Font(family="Georgia", size=17, weight="bold"),
            "cover_small": tkfont.Font(family="Georgia", size=8, weight="bold"),
        }

    def _round_rect(
        self,
        x1: float,
        y1: float,
        x2: float,
        y2: float,
        radius: float = 8,
        fill: str = "",
        outline: str = "",
        width: int = 1,
    ) -> int:
        points = [
            x1 + radius,
            y1,
            x2 - radius,
            y1,
            x2,
            y1,
            x2,
            y1 + radius,
            x2,
            y2 - radius,
            x2,
            y2,
            x2 - radius,
            y2,
            x1 + radius,
            y2,
            x1,
            y2,
            x1,
            y2 - radius,
            x1,
            y1 + radius,
            x1,
            y1,
        ]
        return self.canvas.create_polygon(
            points,
            smooth=True,
            splinesteps=12,
            fill=fill,
            outline=outline,
            width=width,
        )

    def _text(
        self,
        x: float,
        y: float,
        text: str,
        fill: str = COLORS["text"],
        font: str = "body",
        anchor: str = "nw",
        width: float | None = None,
        justify: str = "left",
    ) -> int:
        return self.canvas.create_text(
            x,
            y,
            text=text,
            fill=fill,
            font=self.fonts[font],
            anchor=anchor,
            width=width,
            justify=justify,
        )

    def _button(
        self,
        x1: float,
        y1: float,
        x2: float,
        y2: float,
        label: str,
        action: str,
        payload: str | None = None,
        *,
        fill: str = COLORS["panel_soft"],
        active_fill: str | None = None,
        text_fill: str = COLORS["text"],
        radius: int = 8,
        font: str = "button",
        icon: str | None = None,
    ) -> None:
        key = (action, payload)
        hovered = self.hover_action == key
        bg = active_fill if hovered and active_fill else fill
        self._round_rect(x1, y1, x2, y2, radius, fill=bg, outline=COLORS["line_soft"])
        center_y = (y1 + y2) / 2
        if icon:
            label_max = max(20, x2 - x1 - 42)
            label = self._trim(label, label_max, font)
            self._text(x1 + 14, center_y, icon, text_fill, "body", "w")
            self._text(x1 + 36, center_y, label, text_fill, font, "w")
        else:
            label_max = max(20, x2 - x1 - 12)
            label = self._trim(label, label_max, font)
            self._text((x1 + x2) / 2, center_y, label, text_fill, font, "center")
        self.buttons.append(
            {
                "x1": x1,
                "y1": y1,
                "x2": x2,
                "y2": y2,
                "action": action,
                "payload": payload,
            }
        )

    def _book_by_id(self, book_id: str) -> dict:
        if self.extra_books.get(book_id):
            return self.extra_books[book_id]
        if self.api_results:
            for book in self.api_results:
                if book["id"] == book_id:
                    return book
        for book in BOOKS:
            if book["id"] == book_id:
                return book
        return BOOKS[0]

    def _catalog_books(self) -> list[dict]:
        if self.api_results is not None:
            return self.api_results
        return BOOKS

    def _library_books(self) -> list[dict]:
        library_ids = {item["book_id"] for item in DOWNLOADS if item.get("file_path")}
        return [self._book_by_id(book_id) for book_id in library_ids]

    def _query(self) -> str:
        if self.placeholder_active:
            return ""
        return self.search_entry.get().strip().casefold()

    def _reset_results_scroll(self) -> None:
        self.results_scroll = 0

    def _category_chips_metrics(self) -> tuple[list[tuple[str, float]], float]:
        chips: list[tuple[str, float]] = []
        for category in CATEGORIES:
            chip_w = max(32, self.fonts["body_small"].measure(category) + 24)
            chips.append((category, chip_w))
        total_w = sum(chip_w for _, chip_w in chips) + max(0, (len(chips) - 1) * 8)
        return chips, total_w

    def _apply_theme(self) -> None:
        palette = LIGHT_COLORS if self.theme_mode == "light" else DARK_COLORS
        COLORS.clear()
        COLORS.update(palette)
        self.root.configure(bg=COLORS["app"])
        self.canvas.configure(bg=COLORS["app"])
        entry_fg = COLORS["text_muted"] if self.placeholder_active else COLORS["text"]
        self.search_entry.configure(
            bg=COLORS["input_bg"],
            fg=entry_fg,
            insertbackground=COLORS["text"],
        )

    def _t(self, key: str) -> str:
        lang = "en" if self.interface_language == "en" else "uk"
        return UI_STRINGS.get(lang, UI_STRINGS["uk"]).get(key, UI_STRINGS["uk"].get(key, key))

    def _nav_label(self, uk_label: str) -> str:
        mapping = {
            "Головна": "nav_home",
            "Пошук книг": "nav_search",
            "Завантаження": "nav_downloads",
            "Історія": "nav_history",
            "Бібліотека": "nav_library",
            "Обране": "nav_favorites",
            "Налаштування": "nav_settings",
        }
        return self._t(mapping.get(uk_label, "nav_search"))

    def _update_search_placeholder(self) -> None:
        if self.placeholder_active:
            self.search_entry.delete(0, tk.END)
            self.search_entry.insert(0, self._t("search_placeholder"))
            self.search_entry.configure(fg=COLORS["text_muted"])

    def _visible_books(self) -> list[dict]:
        if self.active_nav == "Бібліотека":
            source = self._library_books()
        elif self.active_nav == "Обране":
            source = [self._book_by_id(book_id) for book_id in self.favorites]
        else:
            source = self._catalog_books()

        query = self._query()
        visible = []
        for book in source:
            if self.active_nav not in ("Бібліотека", "Обране"):
                if self.active_category not in ("Усі", "Більше⌄") and self.active_category not in book["categories"]:
                    continue
            if self.filter_format and book["format"] != self.filter_format:
                continue
            if self.filter_language and book["language"] != self.filter_language:
                continue
            if self.filter_rating:
                try:
                    if float(book["rating"]) < float(self.filter_rating):
                        continue
                except ValueError:
                    continue
            haystack = " ".join(
                [
                    book["title"],
                    book["author"],
                    book["meta"],
                    str(book["isbn"]),
                ]
            ).casefold()
            if query and query not in haystack:
                continue
            visible.append(book)
        return visible

    def _run_search(self) -> None:
        query = self._query()
        self._reset_results_scroll()
        if not query:
            self.api_results = None
            self.draw()
            return

        results = self.book_search.search_books(query)
        self.api_results = results
        for book in results:
            self.extra_books[book["id"]] = book
        if results:
            self.selected_book_id = results[0]["id"]
        self.draw()

    def _on_entry_focus_in(self, _event: tk.Event) -> None:
        if self.placeholder_active:
            self.search_entry.delete(0, tk.END)
            self.search_entry.configure(fg=COLORS["text"])
            self.placeholder_active = False

    def _on_entry_focus_out(self, _event: tk.Event) -> None:
        if not self.search_entry.get().strip():
            self.placeholder_active = True
            self.search_entry.configure(fg=COLORS["text_muted"])
            self.search_entry.delete(0, tk.END)
            self.search_entry.insert(0, self._t("search_placeholder"))
            self.draw()

    def _on_search_change(self, _event: tk.Event) -> None:
        if not self.placeholder_active:
            self._reset_results_scroll()
            self.draw()

    def _on_click(self, event: tk.Event) -> None:
        if self.category_scrollbar_bounds:
            x1, y1, x2, y2, max_scroll, thumb_x, thumb_w, track_w = self.category_scrollbar_bounds
            if max_scroll > 0 and y1 <= event.y <= y2:
                if thumb_x <= event.x <= thumb_x + thumb_w:
                    self.scroll_drag = {
                        "kind": "category",
                        "start_mouse": event.x,
                        "start_scroll": self.category_scroll,
                        "thumb_size": thumb_w,
                        "track_size": track_w,
                        "max_scroll": max_scroll,
                    }
                    return
                if x1 <= event.x <= x2:
                    ratio = (event.x - x1) / max(1, x2 - x1)
                    self.category_scroll = max(0, min(max_scroll, round(ratio * max_scroll)))
                    self.draw()
                    return

        if self.results_scrollbar_bounds:
            x1, y1, x2, y2, max_scroll, thumb_y, thumb_h, track_h = self.results_scrollbar_bounds
            if max_scroll > 0 and x1 <= event.x <= x2:
                if thumb_y <= event.y <= thumb_y + thumb_h:
                    self.scroll_drag = {
                        "kind": "results",
                        "start_mouse": event.y,
                        "start_scroll": self.results_scroll,
                        "thumb_size": thumb_h,
                        "track_size": track_h,
                        "max_scroll": max_scroll,
                    }
                    return
                if y1 <= event.y <= y2:
                    ratio = (event.y - y1) / max(1, y2 - y1)
                    self.results_scroll = max(0, min(max_scroll, round(ratio * max_scroll)))
                    self.draw()
                    return

        if self.download_data_scrollbar_bounds:
            x1, y1, x2, y2, max_scroll, thumb_x, thumb_w, track_w = self.download_data_scrollbar_bounds
            if max_scroll > 0 and y1 <= event.y <= y2:
                if thumb_x <= event.x <= thumb_x + thumb_w:
                    self.scroll_drag = {
                        "kind": "download_data",
                        "start_mouse": event.x,
                        "start_scroll": self.download_data_scroll,
                        "thumb_size": thumb_w,
                        "track_size": track_w,
                        "max_scroll": max_scroll,
                    }
                    return
                if x1 <= event.x <= x2:
                    ratio = (event.x - x1) / max(1, x2 - x1)
                    self.download_data_scroll = max(0, min(max_scroll, round(ratio * max_scroll)))
                    self.draw()
                    return

        for handle in self.download_col_resize_handles:
            if handle["x1"] <= event.x <= handle["x2"] and handle["y1"] <= event.y <= handle["y2"]:
                self.scroll_drag = {
                    "kind": "col_resize",
                    "start_mouse": event.x,
                    "col_a": handle["col_a"],
                    "col_b": handle["col_b"],
                    "start_a": getattr(self, f"download_col_{handle['col_a']}_w"),
                    "start_b": getattr(self, f"download_col_{handle['col_b']}_w"),
                    "min_a": handle["min_a"],
                    "min_b": handle["min_b"],
                }
                return

        for button in reversed(self.buttons):
            if button["x1"] <= event.x <= button["x2"] and button["y1"] <= event.y <= button["y2"]:
                self._handle_action(button["action"], button["payload"])
                return

    def _on_drag(self, event: tk.Event) -> None:
        if not self.scroll_drag:
            return

        drag = self.scroll_drag
        travel = max(1, drag["track_size"] - drag["thumb_size"])
        if drag["kind"] == "category":
            delta = event.x - drag["start_mouse"]
            next_scroll = drag["start_scroll"] + delta * drag["max_scroll"] / travel
            next_scroll = max(0, min(drag["max_scroll"], round(next_scroll)))
            if next_scroll != self.category_scroll:
                self.category_scroll = next_scroll
                self.draw()
        elif drag["kind"] == "results":
            delta = event.y - drag["start_mouse"]
            next_scroll = drag["start_scroll"] + delta * drag["max_scroll"] / travel
            next_scroll = max(0, min(drag["max_scroll"], round(next_scroll)))
            if next_scroll != self.results_scroll:
                self.results_scroll = next_scroll
                self.draw()
        elif drag["kind"] == "download_data":
            delta = event.x - drag["start_mouse"]
            next_scroll = drag["start_scroll"] + delta * drag["max_scroll"] / travel
            next_scroll = max(0, min(drag["max_scroll"], round(next_scroll)))
            if next_scroll != self.download_data_scroll:
                self.download_data_scroll = next_scroll
                self.draw()
        elif drag["kind"] == "col_resize":
            delta = round(event.x - drag["start_mouse"])
            new_a = drag["start_a"] + delta
            new_b = drag["start_b"] - delta
            if new_a >= drag["min_a"] and new_b >= drag["min_b"]:
                setattr(self, f"download_col_{drag['col_a']}_w", new_a)
                setattr(self, f"download_col_{drag['col_b']}_w", new_b)
                self.draw()

    def _on_release(self, _event: tk.Event) -> None:
        self.scroll_drag = None

    def _on_mousewheel(self, event: tk.Event) -> str | None:
        if getattr(event, "num", None) == 4:
            direction = -1
        elif getattr(event, "num", None) == 5:
            direction = 1
        else:
            direction = -1 if event.delta > 0 else 1

        if self.category_scroll_bounds:
            x1, y1, x2, y2, max_scroll = self.category_scroll_bounds
            if x1 <= event.x <= x2 and y1 <= event.y <= y2 and max_scroll > 0:
                step = 40
                next_scroll = max(0, min(max_scroll, self.category_scroll + direction * step))
                if next_scroll != self.category_scroll:
                    self.category_scroll = next_scroll
                    self.draw()
                return "break"

        if self.download_data_scroll_bounds:
            x1, y1, x2, y2, max_scroll = self.download_data_scroll_bounds
            if x1 <= event.x <= x2 and y1 <= event.y <= y2 and max_scroll > 0:
                step = 40
                next_scroll = max(0, min(max_scroll, self.download_data_scroll + direction * step))
                if next_scroll != self.download_data_scroll:
                    self.download_data_scroll = next_scroll
                    self.draw()
                return "break"

        if not self.results_scroll_bounds:
            return None

        x1, y1, x2, y2, max_scroll = self.results_scroll_bounds
        if not (x1 <= event.x <= x2 and y1 <= event.y <= y2) or max_scroll <= 0:
            return None

        next_scroll = max(0, min(max_scroll, self.results_scroll + direction))
        if next_scroll != self.results_scroll:
            self.results_scroll = next_scroll
            self.draw()
        return "break"

    def _on_motion(self, event: tk.Event) -> None:
        over_resize = any(
            handle["x1"] <= event.x <= handle["x2"] and handle["y1"] <= event.y <= handle["y2"]
            for handle in self.download_col_resize_handles
        )
        if over_resize:
            if self.canvas.cget("cursor") != "sb_h_double_arrow":
                self.canvas.configure(cursor="sb_h_double_arrow")
            return

        next_hover: tuple[str, str | None] | None = None
        for button in reversed(self.buttons):
            if button["x1"] <= event.x <= button["x2"] and button["y1"] <= event.y <= button["y2"]:
                next_hover = (button["action"], button["payload"])
                break
        if next_hover != self.hover_action:
            self.hover_action = next_hover
            self.canvas.configure(cursor="hand2" if next_hover else "")
            self.draw()

    def _on_leave(self, _event: tk.Event) -> None:
        if self.hover_action:
            self.hover_action = None
            self.canvas.configure(cursor="")
            self.draw()

    def _handle_action(self, action: str, payload: str | None) -> None:
        if action == "nav" and payload:
            self._reset_results_scroll()
            self.active_nav = payload
            self.filter_open = False
            self.description_expanded = False
            if payload != "Пошук книг":
                self.api_results = None
        elif action == "category" and payload:
            self._reset_results_scroll()
            self.active_category = payload
            visible = self._visible_books()
            if visible and self.selected_book_id not in {book["id"] for book in visible}:
                self.selected_book_id = visible[0]["id"]
        elif action == "select_book" and payload:
            self.selected_book_id = payload
            self.description_expanded = False
        elif action == "search":
            self._run_search()
            return
        elif action == "filter":
            self.filter_open = not self.filter_open
        elif action == "filter_option" and payload:
            self._reset_results_scroll()
            if payload == "format:EPUB":
                self.filter_format = "" if self.filter_format == "EPUB" else "EPUB"
            elif payload == "lang:Українська":
                self.filter_language = "" if self.filter_language == "Українська" else "Українська"
            elif payload == "rating:4":
                self.filter_rating = "" if self.filter_rating == "4" else "4"
        elif action == "bookmark" and payload:
            if payload in self.bookmarks:
                self.bookmarks.remove(payload)
            else:
                self.bookmarks.add(payload)
        elif action == "favorite" and payload:
            if payload in self.favorites:
                self.favorites.remove(payload)
            else:
                self.favorites.add(payload)
        elif action == "download" and payload:
            self._start_download(payload)
        elif action == "remove_download" and payload:
            DOWNLOADS[:] = [item for item in DOWNLOADS if item["book_id"] != payload]
        elif action == "show_history":
            self.active_nav = "Історія"
        elif action == "toggle_description":
            self.description_expanded = not self.description_expanded
        elif action == "set_language" and payload in ("uk", "en"):
            self.interface_language = payload
            self._update_search_placeholder()
        elif action == "set_theme" and payload in ("dark", "light"):
            self.theme_mode = payload
            self._apply_theme()
        self.draw()

    def _start_download(self, book_id: str) -> None:
        file_path = self.book_search.get_file_path(self.root)
        if not file_path:
            return

        book = self._book_by_id(book_id)
        for item in DOWNLOADS:
            if item["book_id"] == book_id:
                item["status"] = "Завершено"
                item["date"] = "Щойно"
                item["size"] = book["size"]
                item["progress"] = 100
                item["file_path"] = file_path
                return
        DOWNLOADS.insert(
            0,
            {
                "book_id": book_id,
                "status": "Завершено",
                "date": "Щойно",
                "size": book["size"],
                "progress": 100,
                "file_path": file_path,
            },
        )

    def draw(self) -> None:
        width = max(self.canvas.winfo_width(), 1060)
        height = max(self.canvas.winfo_height(), 700)
        self.canvas.delete("all")
        self.buttons = []
        self.results_scroll_bounds = None
        self.results_scrollbar_bounds = None
        self.category_scroll_bounds = None
        self.category_scrollbar_bounds = None
        self._category_container_geom = None
        self.download_col_resize_handles = []
        self.download_data_scroll_bounds = None
        self.download_data_scrollbar_bounds = None

        self._round_rect(1, 1, width - 2, height - 2, 10, fill=COLORS["app"], outline="#0f2538")
        self._draw_sidebar(height)

        content_x = 215
        content_y = 22
        content_w = width - content_x - 14
        right_w = 398 if content_w > 890 else 350
        gap = 12
        right_x = width - right_w - 14
        left_w = right_x - content_x - gap
        downloads_h = 226
        bottom_margin = 14

        if self.active_nav == "Налаштування":
            self.search_entry.place_forget()
            self._draw_settings(content_x + 10, content_y, left_w + right_w + gap, height - content_y - bottom_margin)
            return

        if self.active_nav == "Історія":
            self.search_entry.place_forget()
            self._draw_full_history(content_x + 10, content_y, left_w + right_w + gap, height - content_y - bottom_margin)
            return

        if self.active_nav == "Завантаження":
            self.search_entry.place_forget()
            self._draw_downloads(content_x + 10, content_y, left_w + right_w + gap, height - content_y - bottom_margin)
            return

        if self.active_nav == "Головна":
            self.search_entry.place_forget()
            self._draw_home(content_x + 10, content_y, left_w - 10, right_x, right_w, height - content_y - bottom_margin)
            return

        search_x = content_x + 10
        search_y = content_y
        left_content_w = left_w - 10
        category_y = search_y + 44 + 10
        self._draw_category_container(search_x, category_y, left_content_w)

        self._draw_sidebar(height)
        self._draw_search_bar(search_x, search_y, left_content_w)
        panel_top = category_y + self._category_container_height() + 10
        self._search_area_bottom = category_y + self._category_container_height()
        results_h = max(342, height - panel_top - downloads_h - 24)
        self._draw_results(search_x, panel_top, left_content_w, results_h)
        self._draw_downloads(search_x, panel_top + results_h + 10, left_content_w, downloads_h)
        self._draw_details(right_x, panel_top, right_w, height - panel_top - bottom_margin)
        self._draw_category_side_masks()
        self._draw_filter_button(right_x, right_w, category_y)

    def _draw_sidebar(self, height: float) -> None:
        sidebar_w = 195
        self.canvas.create_rectangle(0, 0, sidebar_w, height, fill=COLORS["sidebar"], outline="")
        self.canvas.create_line(sidebar_w, 0, sidebar_w, height, fill="#0f2438")

        self._round_rect(17, 19, 34, 36, 4, fill=COLORS["blue"], outline="")
        self._text(24.5, 25.5, "▥", "#d9efff", "caption", "center")
        self._text(44, 20, "BookDownloader", COLORS["text"], "brand")

        y = 64
        for icon, label in SIDEBAR_ITEMS:
            if label == "Налаштування":
                self.canvas.create_line(18, y - 12, sidebar_w - 20, y - 12, fill=COLORS["line_soft"])
            active = label == self.active_nav
            row_h = 38
            fill = COLORS["sidebar_active"] if active else COLORS["sidebar"]
            text_fill = COLORS["blue"] if active else COLORS["text_soft"]
            if active:
                self._round_rect(10, y, sidebar_w - 10, y + row_h, 5, fill=fill, outline="")
                self.canvas.create_rectangle(9, y + 4, 12, y + row_h - 4, fill=COLORS["blue"], outline="")
            self._text(26, y + row_h / 2, icon, text_fill, "body", "center")
            self._text(44, y + row_h / 2, self._trim(self._nav_label(label), sidebar_w - 56, "nav"), text_fill, "nav", "w")
            self.buttons.append(
                {"x1": 9, "y1": y, "x2": sidebar_w - 10, "y2": y + row_h, "action": "nav", "payload": label}
            )
            y += 52

        storage_y = height - 64
        self._text(21, storage_y, "Сховище", COLORS["text_soft"], "body_small")
        self._round_rect(21, storage_y + 18, 174, storage_y + 23, 3, fill="#15253a", outline="")
        self._round_rect(21, storage_y + 18, 88, storage_y + 23, 3, fill=COLORS["blue"], outline="")
        self._text(21, storage_y + 32, "18.4 ГБ / 50 ГБ", COLORS["text_soft"], "body_small")

    def _category_container_height(self) -> float:
        return 10 + 27 + 8 + 6 + 10

    def _draw_search_bar(self, x: float, y: float, left_w: float) -> None:
        search_w = min(620, max(420, left_w - 10))
        search_label = self._t("search")
        search_button_w = 36 + self.fonts["button"].measure(search_label) + 14
        search_h = 44
        self._round_rect(x, y, x + search_w + 400, y + search_h, 7, fill=COLORS["input_bg"], outline=COLORS["input_line"])
        self.search_entry.place(x=x + 16, y=y + 11, width=search_w + 275, height=22)
        self._button(
            x + search_w + 300,
            y + 1,
            x + search_w + 400,
            y + search_h - 1,
            self._t("search"),
            "search",
            fill=COLORS["blue"],
            active_fill=COLORS["blue_dark"],
            radius=7,
            font="button",
            icon="⌕",
        )

    def _draw_filter_button(self, right_x: float, right_w: float, category_y: float) -> None:
        filter_label = "Фільтри" if not self.filter_open else "Фільтри: відкрито"
        filter_h = 34
        container_h = self._category_container_height()
        filter_y = category_y + (container_h - filter_h) / 2
        self._button(
            right_x - 150,
            filter_y,
            right_x + min(-20, right_w - 16),
            filter_y + filter_h,
            filter_label,
            "filter",
            fill=COLORS["panel_alt"],
            active_fill=COLORS["panel_soft"],
            radius=7,
            icon="≡",
        )

    def _draw_category_side_masks(self) -> None:
        if not self._category_container_geom:
            return

        geom = self._category_container_geom
        side_w = 29
        app = COLORS["app"]
        chip_y = geom["chip_y"]
        chip_y2 = chip_y + geom["chip_h"] + 1

        self.canvas.create_rectangle(
            geom["x"] - side_w,
            chip_y,
            geom["x"],
            chip_y2,
            fill=app,
            outline="",
        )
        self.canvas.create_rectangle(
            geom["x"] + geom["w"] + 1,
            chip_y,
            geom["x"] + geom["w"] + side_w + 50,
            chip_y2,
            fill=app,
            outline="",
        )

    def _draw_category_container(self, x: float, y: float, w: float) -> float:
        pad_x = 12
        pad_y = 10
        chip_h = 27
        scroll_h = 6
        scroll_gap = 8
        container_h = self._category_container_height()

        self._round_rect(x, y, x + w, y + container_h, 8, fill=COLORS["panel"], outline=COLORS["line_soft"])

        viewport_x = x + pad_x
        viewport_w = w - pad_x * 2
        chip_y = y + pad_y

        chips, total_w = self._category_chips_metrics()
        max_scroll = max(0, int(total_w - viewport_w))
        self.category_scroll = max(0, min(self.category_scroll, max_scroll))
        has_scroll = max_scroll > 0
        self.category_scroll_bounds = (x, y, x + w, y + container_h, max_scroll)
        self._category_container_geom = {
            "x": x,
            "y": y,
            "w": w,
            "h": container_h,
            "viewport_x": viewport_x,
            "viewport_w": viewport_w,
            "chip_y": chip_y,
            "chip_h": chip_h,
        }

        chip_x = viewport_x - self.category_scroll
        for category, chip_w in chips:
            chip_right = chip_x + chip_w
            if chip_right > viewport_x and chip_x < viewport_x + viewport_w:
                active = self.active_category == category
                fill = COLORS["blue"] if active else COLORS["panel_alt"]
                text_fill = COLORS["text"] if active else COLORS["text_soft"]
                self._button(
                    chip_x,
                    chip_y,
                    chip_x + chip_w,
                    chip_y + chip_h,
                    category,
                    "category",
                    category,
                    fill=fill,
                    active_fill=COLORS["blue_dark"] if active else COLORS["panel_soft"],
                    text_fill=text_fill,
                    radius=7,
                    font="body_small",
                )
            chip_x += chip_w + 8

        if has_scroll:
            track_x1 = viewport_x
            track_x2 = viewport_x + viewport_w
            track_y1 = y + container_h - pad_y - scroll_h
            track_y2 = track_y1 + scroll_h
            track_w = max(1, track_x2 - track_x1)
            thumb_w = max(28, track_w * viewport_w / total_w)
            thumb_x = track_x1 + (track_w - thumb_w) * self.category_scroll / max(1, max_scroll)
            self._round_rect(track_x1, track_y1, track_x2, track_y2, 3, fill=COLORS["line_soft"], outline="")
            self._round_rect(thumb_x, track_y1, thumb_x + thumb_w, track_y2, 3, fill=COLORS["blue"], outline="")
            self.category_scrollbar_bounds = (
                track_x1,
                track_y1 - 4,
                track_x2,
                track_y2 + 4,
                max_scroll,
                thumb_x,
                thumb_w,
                track_w,
            )

        return y + container_h

    def _draw_results(self, x: float, y: float, w: float, h: float) -> None:
        self._round_rect(x, y, x + w, y + h, 8, fill=COLORS["panel"], outline=COLORS["line_soft"])
        self._text(x + 14, y + 14, "Результати пошуку", COLORS["text"], "section")

        books = self._visible_books()
        selected_ids = {book["id"] for book in books}
        if books and self.selected_book_id not in selected_ids:
            self.selected_book_id = books[0]["id"]

        row_x = x + 14
        row_y = y + 40
        row_h = 87
        max_rows = max(1, int((h - 50) // row_h))
        max_scroll = max(0, len(books) - max_rows)
        self.results_scroll = max(0, min(self.results_scroll, max_scroll))
        has_scroll = max_scroll > 0
        row_w = w - (42 if has_scroll else 28)
        self.results_scroll_bounds = (x, y, x + w, y + h, max_scroll)
        if not books:
            self._text(
                x + w / 2,
                y + h / 2,
                "Нічого не знайдено",
                COLORS["text_soft"],
                "title",
                "center",
            )
            self._text(
                x + w / 2,
                y + h / 2 + 24,
                "Спробуйте іншу назву, автора або ISBN.",
                COLORS["text_muted"],
                "body_small",
                "center",
            )
            return

        visible_books = books[self.results_scroll : self.results_scroll + max_rows]
        for index, book in enumerate(visible_books):
            top = row_y + index * row_h
            active = book["id"] == self.selected_book_id
            fill = COLORS["panel_alt"] if active else COLORS["panel"]
            if active:
                self._round_rect(row_x, top, row_x + row_w, top + row_h - 9, 6, fill=fill, outline="")
            else:
                self.canvas.create_line(row_x, top + row_h - 8, row_x + row_w, top + row_h - 8, fill=COLORS["line_soft"])
            btn_w = 112
            btn_x = row_x + row_w - btn_w - 22
            self.buttons.append(
                {
                    "x1": row_x,
                    "y1": top,
                    "x2": btn_x - 8,
                    "y2": top + row_h - 9,
                    "action": "select_book",
                    "payload": book["id"],
                }
            )
            self._draw_cover(row_x + 8, top + 9, 52, 70, book, small=True)

            text_x = row_x + 74
            text_max_w = max(80, btn_x - text_x - 8)
            self._text_fit(text_x, top + 11, book["title"], COLORS["text"], "title", "w", text_max_w)
            self._text_fit(text_x, top + 35, book["author"], COLORS["text_soft"], "body_small", "w", text_max_w)
            meta = f"{book['meta']}  •  {book['pages']} стор."
            self._text_fit(text_x, top + 56, meta, COLORS["text_muted"], "body_small", "w", text_max_w)
            self._text_fit(text_x, top + 72, f"ISBN: {book['isbn']}", COLORS["text_muted"], "caption", "w", text_max_w)

            self._button(
                btn_x,
                top + 18,
                btn_x + btn_w,
                top + 52,
                "Завантажити",
                "download",
                book["id"],
                fill=COLORS["panel_soft"],
                active_fill="#1c334d",
                radius=6,
                icon="⇩",
            )
            self._text_fit(
                btn_x + (btn_w / 2),
                top + 66,
                f"{book['format']}  •  {book['size']}",
                COLORS["text_muted"],
                "caption",
                "center",
                btn_w - 8,
            )

        if has_scroll:
            track_x = x + w - 17
            track_y1 = row_y
            track_y2 = y + h - 14
            track_h = max(1, track_y2 - track_y1)
            thumb_h = max(28, track_h * max_rows / len(books))
            thumb_y = track_y1 + (track_h - thumb_h) * self.results_scroll / max(1, max_scroll)
            self._round_rect(track_x, track_y1, track_x + 6, track_y2, 3, fill=COLORS["line_soft"], outline="")
            self._round_rect(track_x, thumb_y, track_x + 6, thumb_y + thumb_h, 3, fill=COLORS["blue"], outline="")
            self.results_scrollbar_bounds = (
                track_x - 8,
                track_y1,
                track_x + 14,
                track_y2,
                max_scroll,
                thumb_y,
                thumb_h,
                track_h,
            )

    def _draw_downloads(self, x: float, y: float, w: float, h: float) -> None:
        self._round_rect(x, y, x + w, y + h, 8, fill=COLORS["panel"], outline=COLORS["line_soft"])
        self._text(x + 14, y + 14, self._t("download_history"), COLORS["text"], "section")
        history_text = self._t("view_all_history")
        history_label = self.fonts["body_small"].measure(history_text)
        history_x2 = x + w - 14
        history_x1 = history_x2 - history_label
        self._text(history_x2, y + 15, history_text, COLORS["blue"], "body_small", "ne")
        self.buttons.append(
            {
                "x1": history_x1 - 4,
                "y1": y + 8,
                "x2": history_x2 + 4,
                "y2": y + 28,
                "action": "show_history",
                "payload": None,
            }
        )

        items = DOWNLOADS if h > 180 else DOWNLOADS[:4]
        self._draw_download_preview_rows(x + 14, y + 38, w - 28, h - 50, items)

    def _download_preview_row_height(self, book: dict, title_col_w: float) -> int:
        title_lines = self._wrap_text(book["title"], title_col_w - 4, "body_small")
        author_lines = self._wrap_text(book["author"], title_col_w - 4, "caption")[:2]
        title_lh = self._line_height("body_small")
        author_lh = self._line_height("caption")
        return max(54, int(6 + len(title_lines) * title_lh + 2 + len(author_lines) * author_lh + 8))

    def _download_data_content_width(self) -> float:
        gap = 8
        return (
            self.download_col_status_w
            + gap
            + self.download_col_date_w
            + gap
            + self.download_col_size_w
            + gap
            + 56
        )

    def _download_data_columns_at(self, data_x: float) -> dict[str, float | int]:
        gap = 8
        actions_w = 56
        status_w = self.download_col_status_w
        date_w = self.download_col_date_w
        size_w = self.download_col_size_w
        status_x1 = data_x
        date_x1 = status_x1 + status_w + gap
        size_x1 = date_x1 + date_w + gap
        actions_x1 = size_x1 + size_w + gap
        return {
            "status_x1": status_x1,
            "status_w": status_w,
            "date_x1": date_x1,
            "date_w": date_w,
            "size_x1": size_x1,
            "size_w": size_w,
            "actions_x1": actions_x1,
            "actions_w": actions_w,
            "content_w": actions_x1 + actions_w - data_x,
        }

    def _download_preview_title_width(self, items: list[dict], panel_w: float) -> float:
        if not items:
            return 120
        longest = max(
            self.fonts["body_small"].measure(self._book_by_id(item["book_id"])["title"]) for item in items
        )
        return max(100, min(longest + 10, int(panel_w * 0.48)))

    def _draw_download_preview_rows(
        self,
        x: float,
        y: float,
        w: float,
        h: float,
        items: list[dict],
    ) -> None:
        if not items:
            return

        cover_w = 44
        title_x = x + cover_w
        title_col_w = self._download_preview_title_width(items, w)
        title_block_end = title_x + title_col_w
        title_data_gap = 20
        data_content_w = self._download_data_content_width()
        data_viewport_w = max(100, x + w - title_block_end - title_data_gap)
        data_viewport_x = x + w - data_viewport_w
        if data_viewport_x < title_block_end + title_data_gap:
            data_viewport_x = title_block_end + title_data_gap
            data_viewport_w = max(80, x + w - data_viewport_x)
        max_scroll = max(0, int(data_content_w - data_viewport_w))
        self.download_data_scroll = max(0, min(self.download_data_scroll, max_scroll))
        has_h_scroll = max_scroll > 0
        scroll_bar_h = 8 if has_h_scroll else 0
        self.download_data_scroll_bounds = (
            data_viewport_x,
            y,
            data_viewport_x + data_viewport_w,
            y + h,
            max_scroll,
        )

        row_y = y
        scroll = self.download_data_scroll
        title_lh = self._line_height("body_small")
        for index, item in enumerate(items):
            book = self._book_by_id(item["book_id"])
            is_done = item["progress"] >= 100
            row_h = self._download_preview_row_height(book, title_col_w)
            if row_y + row_h > y + h - scroll_bar_h:
                break
            top = row_y

            if index > 0:
                self.canvas.create_line(x, top - 3, x + w, top - 3, fill=COLORS["line_soft"])

            self._draw_cover(x + 8, top + max(4, (row_h - 38) / 2), 28, 38, book, small=True)
            title_lines = self._wrap_text(book["title"], title_col_w - 4, "body_small")
            for line_i, line in enumerate(title_lines):
                self._text(title_x, top + 6 + line_i * title_lh, line, COLORS["text"], "body_small", "nw")
            author_y = top + 6 + len(title_lines) * title_lh + 2
            author_lines = self._wrap_text(book["author"], title_col_w - 4, "caption")[:2]
            author_lh = self._line_height("caption")
            for line_i, line in enumerate(author_lines):
                self._text(title_x, author_y + line_i * author_lh, line, COLORS["text_muted"], "caption", "nw")
            self._draw_download_data_row(
                item,
                book,
                data_viewport_x,
                data_viewport_w,
                data_content_w,
                scroll,
                top,
                row_h,
                is_done,
                x + w,
            )
            self.canvas.create_rectangle(
                x,
                top,
                data_viewport_x,
                top + row_h,
                fill=COLORS["panel"],
                outline="",
            )
            self._draw_cover(x + 8, top + max(4, (row_h - 38) / 2), 28, 38, book, small=True)
            for line_i, line in enumerate(title_lines):
                self._text(title_x, top + 6 + line_i * title_lh, line, COLORS["text"], "body_small", "nw")
            for line_i, line in enumerate(author_lines):
                self._text(title_x, author_y + line_i * author_lh, line, COLORS["text_muted"], "caption", "nw")
            row_y += row_h

        if row_y > y:
            self.canvas.create_line(
                data_viewport_x,
                y,
                data_viewport_x,
                min(row_y, y + h - scroll_bar_h),
                fill=COLORS["line_soft"],
            )

        if has_h_scroll:
            track_x1 = data_viewport_x
            track_x2 = data_viewport_x + data_viewport_w
            track_y1 = y + h - scroll_bar_h - 2
            track_y2 = track_y1 + scroll_bar_h
            track_w = max(1, track_x2 - track_x1)
            thumb_w = max(28, track_w * data_viewport_w / data_content_w)
            thumb_x = track_x1 + (track_w - thumb_w) * self.download_data_scroll / max(1, max_scroll)
            self._round_rect(track_x1, track_y1, track_x2, track_y2, 3, fill=COLORS["line_soft"], outline="")
            self._round_rect(thumb_x, track_y1, thumb_x + thumb_w, track_y2, 3, fill=COLORS["blue"], outline="")
            self.download_data_scrollbar_bounds = (
                track_x1,
                track_y1 - 4,
                track_x2,
                track_y2 + 4,
                max_scroll,
                thumb_x,
                thumb_w,
                track_w,
            )

    def _draw_download_data_row(
        self,
        item: dict,
        book: dict,
        viewport_x: float,
        viewport_w: float,
        content_w: float,
        scroll: float,
        top: float,
        row_h: float,
        is_done: bool,
        panel_right: float,
    ) -> None:
        data_x = viewport_x - scroll
        cols = self._download_data_columns_at(data_x)
        data_right = data_x + content_w

        if data_right > viewport_x and data_x < viewport_x + viewport_w:
            status_color = COLORS["text_soft"] if is_done else COLORS["blue"]
            status_y = top + (row_h / 2)
            if cols["status_x1"] + cols["status_w"] > viewport_x and cols["status_x1"] < viewport_x + viewport_w:
                self._text(cols["status_x1"], status_y, "●", status_color, "body_small", "w")
                self._text_fit(
                    cols["status_x1"] + 14,
                    status_y,
                    item["status"],
                    status_color,
                    "caption",
                    "w",
                    cols["status_w"] - 18,
                )

            if is_done and item.get("date"):
                if cols["date_x1"] + cols["date_w"] > viewport_x and cols["date_x1"] < viewport_x + viewport_w:
                    self._text_fit(
                        cols["date_x1"],
                        status_y,
                        item["date"],
                        COLORS["text_muted"],
                        "caption",
                        "w",
                        cols["date_w"],
                    )

            size_x = cols["size_x1"] + cols["size_w"]
            if cols["size_x1"] < viewport_x + viewport_w and size_x > viewport_x:
                self._text_fit(
                    size_x,
                    top + 8,
                    item["size"],
                    COLORS["text_muted"],
                    "caption",
                    "e",
                    cols["size_w"],
                )

            if not is_done:
                bar_x1 = cols["status_x1"] + 14
                if bar_x1 + 120 > viewport_x and bar_x1 < viewport_x + viewport_w:
                    self._round_rect(bar_x1, top + row_h - 16, bar_x1 + 92, top + row_h - 12, 3, fill="#132741", outline="")
                    progress_w = 92 * item["progress"] / 100
                    self._round_rect(bar_x1, top + row_h - 16, bar_x1 + progress_w, top + row_h - 12, 3, fill=COLORS["blue"], outline="")
                    self._text(bar_x1 + 98, top + 8, f"{item['progress']}%", COLORS["text_muted"], "caption")

            actions_x1 = cols["actions_x1"]
            if actions_x1 + cols["actions_w"] > viewport_x and actions_x1 < viewport_x + viewport_w:
                btn_x1 = max(viewport_x, actions_x1)
                btn_x2 = min(viewport_x + viewport_w, actions_x1 + cols["actions_w"])
                self._text(actions_x1 + 8, top + row_h / 2, "□", COLORS["text_muted"], "body_small", "center")
                pause_or_close = "Ⅱ" if not is_done else "×"
                self._text(actions_x1 + 40, top + row_h / 2, pause_or_close, COLORS["text_muted"], "body", "center")
                self.buttons.append(
                    {
                        "x1": btn_x1,
                        "y1": top,
                        "x2": btn_x2,
                        "y2": top + row_h - 4,
                        "action": "remove_download",
                        "payload": book["id"],
                    }
                )

        if viewport_x + viewport_w < panel_right:
            self.canvas.create_rectangle(
                viewport_x + viewport_w,
                top,
                panel_right,
                top + row_h,
                fill=COLORS["panel"],
                outline="",
            )

    def _download_columns(self, x: float, w: float) -> dict[str, float | int]:
        actions_w = 56
        gap = 8
        size_w = self.download_col_size_w
        date_w = self.download_col_date_w
        status_w = self.download_col_status_w
        right = x + w
        size_x2 = right - actions_w
        size_x1 = size_x2 - size_w
        date_x2 = size_x1 - gap
        date_x1 = date_x2 - date_w
        status_x2 = date_x1 - gap
        status_x1 = status_x2 - status_w
        text_start = x + 47
        text_max = max(60, status_x1 - text_start - 8)
        return {
            "text_start": text_start,
            "text_max": text_max,
            "status_x1": status_x1,
            "status_w": status_w,
            "date_x1": date_x1,
            "date_w": date_w,
            "size_x1": size_x1,
            "size_w": size_w,
            "actions_x1": size_x2,
        }

    def _draw_download_table_header(self, x: float, y: float, w: float) -> None:
        cols = self._download_columns(x, w)
        self._text(cols["status_x1"], y + 2, "Статус", COLORS["text_muted"], "caption")
        self._text(cols["date_x1"], y + 2, "Дата", COLORS["text_muted"], "caption")
        self._text(cols["size_x1"], y + 2, "Розмір", COLORS["text_muted"], "caption")
        self.canvas.create_line(x, y + 18, x + w, y + 18, fill=COLORS["line_soft"])

        gap = 8
        boundaries = [
            (cols["date_x1"] - gap // 2, "status", "date", 72, 80),
            (cols["size_x1"] - gap // 2, "date", "size", 80, 56),
        ]
        for boundary, col_a, col_b, min_a, min_b in boundaries:
            handle_half = 4
            self.canvas.create_line(boundary, y, boundary, y + 18, fill=COLORS["line"], width=1)
            self.download_col_resize_handles.append(
                {
                    "x1": boundary - handle_half,
                    "y1": y,
                    "x2": boundary + handle_half,
                    "y2": y + 20,
                    "col_a": col_a,
                    "col_b": col_b,
                    "min_a": min_a,
                    "min_b": min_b,
                }
            )

    def _draw_download_rows(
        self,
        x: float,
        y: float,
        w: float,
        _h: float,
        items: list[dict],
        *,
        table_mode: bool = False,
    ) -> None:
        row_y = y
        compact = w < 760 and not table_mode
        row_h = 54 if compact else 44
        cols = self._download_columns(x, w)
        for index, item in enumerate(items):
            book = self._book_by_id(item["book_id"])
            top = row_y + index * row_h
            if index > 0:
                self.canvas.create_line(x, top - 3, x + w, top - 3, fill=COLORS["line_soft"])

            self._draw_cover(x + 8, top + (6 if compact else 0), 28, 38, book, small=True)
            is_done = item["progress"] >= 100

            if compact:
                self._text_fit(
                    cols["text_start"],
                    top + 4,
                    book["title"],
                    COLORS["text"],
                    "body_small",
                    "w",
                    cols["text_max"],
                )
                secondary = book["author"]
                self._text_fit(
                    cols["text_start"],
                    top + 22,
                    secondary,
                    COLORS["text_muted"],
                    "caption",
                    "w",
                    cols["text_max"],
                )
                self._text_fit(
                    cols["size_x1"] + cols["size_w"],
                    top + 4,
                    item["size"],
                    COLORS["text_muted"],
                    "caption",
                    "e",
                    cols["size_w"],
                )
                status_color = COLORS["text_soft"] if is_done else COLORS["blue"]
                self._text(cols["status_x1"], top + 22, "●", status_color, "body_small", "w")
                self._text_fit(
                    cols["status_x1"] + 14,
                    top + 22,
                    item["status"],
                    status_color,
                    "caption",
                    "w",
                    cols["status_w"] - 18,
                )
                if is_done and item.get("date"):
                    self._text_fit(
                        cols["date_x1"],
                        top + 22,
                        item["date"],
                        COLORS["text_muted"],
                        "caption",
                        "w",
                        cols["date_w"],
                    )
            else:
                self._text_fit(
                    cols["text_start"],
                    top + 2,
                    book["title"],
                    COLORS["text"],
                    "body_small",
                    "w",
                    cols["text_max"],
                )
                self._text_fit(
                    cols["text_start"],
                    top + 20,
                    book["author"],
                    COLORS["text_muted"],
                    "caption",
                    "w",
                    cols["text_max"],
                )
                status_color = COLORS["text_soft"] if is_done else COLORS["blue"]
                self._text(cols["status_x1"], top + 16, "●", status_color, "body_small", "w")
                self._text_fit(
                    cols["status_x1"] + 14,
                    top + 8,
                    item["status"],
                    status_color,
                    "caption",
                    "w",
                    cols["status_w"] - 18,
                )
                if is_done and item.get("date"):
                    self._text_fit(
                        cols["date_x1"],
                        top + (10 if table_mode else 12),
                        item["date"],
                        COLORS["text_soft"],
                        "body_small" if table_mode else "caption",
                        "w",
                        cols["date_w"],
                    )
                self._text_fit(
                    cols["size_x1"] + cols["size_w"],
                    top + 12,
                    item["size"],
                    COLORS["text_muted"],
                    "caption",
                    "e",
                    cols["size_w"],
                )

            if not is_done:
                bar_x1 = cols["status_x1"] + 14
                self._round_rect(bar_x1, top + 27, bar_x1 + 92, top + 31, 3, fill="#132741", outline="")
                progress_w = 92 * item["progress"] / 100
                self._round_rect(bar_x1, top + 27, bar_x1 + progress_w, top + 31, 3, fill=COLORS["blue"], outline="")
                self._text(bar_x1 + 98, top + 8, f"{item['progress']}%", COLORS["text_muted"], "caption")

            self._text(x + w - 58, top + 16, "□", COLORS["text_muted"], "body_small", "center")
            pause_or_close = "Ⅱ" if not is_done else "×"
            self._text(x + w - 25, top + 16, pause_or_close, COLORS["text_muted"], "body", "center")
            self.buttons.append(
                {
                    "x1": x + w - 28,
                    "y1": top,
                    "x2": x + w - 4,
                    "y2": top + 36,
                    "action": "remove_download",
                    "payload": book["id"],
                }
            )

    def _draw_details(self, x: float, y: float, w: float, h: float) -> None:
        self._round_rect(x, y, x + w, y + h, 8, fill=COLORS["panel"], outline=COLORS["line_soft"])
        book = self._book_by_id(self.selected_book_id)

        cover_x = x + 20
        cover_y = y + 24
        self._draw_cover(cover_x, cover_y, 120, 180, book, small=False)

        info_x = cover_x + 140
        info_max_w = max(80, x + w - 20 - info_x)
        self._text_fit(info_x, cover_y + 6, book["title"], COLORS["text"], "detail_title", "w", info_max_w)
        detail_lines = [
            book["author"],
            book["meta"],
            f"Мова: {book['language']}",
            f"Формат: {book['format']}",
            f"Розмір: {book['size']}",
            f"Сторінок: {book['pages']}",
            f"ISBN: {book['isbn']}",
        ]
        detail_y = cover_y + 48
        detail_gap = 16
        for i, line in enumerate(detail_lines):
            self._text_fit(info_x, detail_y + i * detail_gap, line, COLORS["text_soft"], "body_small", "w", info_max_w)

        self._text(info_x, cover_y + 150, "★★★★★", COLORS["yellow"], "body")
        self._text_fit(
            info_x,
            cover_y + 186,
            f"{book['rating']} ({book['reviews']} оцінок)",
            COLORS["text_soft"],
            "body_small",
            "w",
            info_max_w,
        )

        action_y = cover_y + 228
        bookmarked = book["id"] in self.bookmarks
        favorited = book["id"] in self.favorites
        self._button(
            x + 20,
            action_y,
            x + w - 148,
            action_y + 38,
            "Завантажити",
            "download",
            book["id"],
            fill=COLORS["blue"],
            active_fill=COLORS["blue_dark"],
            radius=6,
            icon="⇩",
        )
        self._button(
            x + w - 136,
            action_y,
            x + w - 82,
            action_y + 38,
            "▣" if bookmarked else "□",
            "bookmark",
            book["id"],
            fill=COLORS["panel_soft"],
            active_fill="#1c334d",
            radius=6,
        )
        self._button(
            x + w - 70,
            action_y,
            x + w - 16,
            action_y + 38,
            "♥" if favorited else "♡",
            "favorite",
            book["id"],
            fill=COLORS["panel_soft"],
            active_fill="#1c334d",
            radius=6,
            text_fill=COLORS["danger"] if favorited else COLORS["text_soft"],
        )

        desc_y = action_y + 66
        self._text(x + 20, desc_y, "Опис", COLORS["text"], "section")
        description = book["description"]
        if not self.description_expanded:
            self._text_fit(
                x + 20,
                desc_y + 34,
                description,
                COLORS["text_soft"],
                "body_small",
                "w",
                w - 40,
            )
        else:
            self._text_block(x + 20, desc_y + 34, description, COLORS["text_soft"], "body_small", w - 40, max_lines=4)
        more_label = "Показати менше  ⌃" if self.description_expanded else "Показати більше  ⌄"
        self._text(x + 20, desc_y + 100, more_label, COLORS["blue"], "body_small")
        self.buttons.append(
            {
                "x1": x + 20,
                "y1": desc_y + 94,
                "x2": x + 180,
                "y2": desc_y + 118,
                "action": "toggle_description",
                "payload": None,
            }
        )

        line_y = desc_y + 138
        self.canvas.create_line(x + 20, line_y, x + w - 20, line_y, fill=COLORS["line_soft"])

        info_y = line_y + 22
        self._text(x + 20, info_y, "Інформація про файл", COLORS["text"], "section")
        rows = [
            ("Формат", book["format"]),
            ("Розмір файлу", book["size"]),
            ("Дата публікації", book["date"]),
            ("Видавництво", book["publisher"]),
        ]
        download_item = next((item for item in DOWNLOADS if item["book_id"] == book["id"]), None)
        if download_item and download_item.get("file_path"):
            rows.append(("Шлях до файлу", download_item["file_path"]))
        row_gap = 26
        max_rows = max(0, int((y + h - 20 - (info_y + 42)) // row_gap) + 1)
        for i, (label, value) in enumerate(rows[:max_rows]):
            row_y = info_y + 42 + i * row_gap
            label_max_w = max(90, min(w * 0.38, 150))
            value_max_w = max(80, w - 56 - label_max_w)
            self._text_fit(x + 20, row_y, label, COLORS["text_muted"], "body_small", "w", label_max_w)
            self._text_fit(x + w - 20, row_y, value, COLORS["text_soft"], "body_small", "ne", value_max_w)

        if self.filter_open:
            self._draw_filter_popover(x - 170, y + 76)

    def _draw_filter_popover(self, x: float, y: float) -> None:
        self._round_rect(x, y, x + 150, y + 116, 8, fill="#0d1827", outline=COLORS["line"])
        self._text(x + 12, y + 12, "Швидкі фільтри", COLORS["text"], "section")
        options = [
            ("EPUB", "format:EPUB", 42),
            ("Українська мова", "lang:Українська", 65),
            ("4+ зірки", "rating:4", 88),
        ]
        for label, payload, row_y in options:
            active = (
                (payload == "format:EPUB" and self.filter_format == "EPUB")
                or (payload == "lang:Українська" and self.filter_language == "Українська")
                or (payload == "rating:4" and self.filter_rating == "4")
            )
            fill = COLORS["blue"] if active else COLORS["text_soft"]
            self._text_fit(x + 12, y + row_y, label, fill, "body_small", "w", 126)
            self.buttons.append(
                {
                    "x1": x + 8,
                    "y1": y + row_y - 8,
                    "x2": x + 142,
                    "y2": y + row_y + 14,
                    "action": "filter_option",
                    "payload": payload,
                }
            )

    def _draw_home(self, x: float, y: float, left_w: float, right_x: float, right_w: float, h: float) -> None:
        self._round_rect(x, y, x + left_w, y + h, 8, fill=COLORS["panel"], outline=COLORS["line_soft"])
        self._text_fit(x + 20, y + 24, "Ласкаво просимо до BookDownloader", COLORS["text"], "detail_title", "w", left_w - 40)
        self._text_fit(
            x + 20,
            y + 72,
            "Оберіть розділ зліва або перейдіть до пошуку книг.",
            COLORS["text_soft"],
            "body",
            "w",
            left_w - 40,
        )
        stats_y = y + 120
        self._text(x + 20, stats_y, f"Книг у каталозі: {len(BOOKS)}", COLORS["text_soft"], "body_small")
        self._text(x + 20, stats_y + 24, f"Завантажень: {len(DOWNLOADS)}", COLORS["text_soft"], "body_small")
        self._text(x + 20, stats_y + 48, f"У бібліотеці: {len(self._library_books())}", COLORS["text_soft"], "body_small")
        self._text(x + 20, stats_y + 72, f"В обраному: {len(self.favorites)}", COLORS["text_soft"], "body_small")
        self._button(
            x + 20,
            stats_y + 110,
            x + 180,
            stats_y + 146,
            "Перейти до пошуку",
            "nav",
            "Пошук книг",
            fill=COLORS["blue"],
            active_fill=COLORS["blue_dark"],
            radius=6,
        )
        self._draw_details(right_x, y, right_w, h)

    def _draw_full_history(self, x: float, y: float, w: float, h: float) -> None:
        self._round_rect(x, y, x + w, y + h, 8, fill=COLORS["panel"], outline=COLORS["line_soft"])
        self._text(x + 14, y + 14, self._t("full_history"), COLORS["text"], "section")
        table_x = x + 14
        table_w = w - 28
        header_y = y + 40
        rows_y = y + 62
        self._draw_download_table_header(table_x, header_y, table_w)
        self._draw_download_rows(table_x, rows_y, table_w, h - 76, DOWNLOADS, table_mode=True)

    def _draw_settings(self, x: float, y: float, w: float, h: float) -> None:
        self._round_rect(x, y, x + w, y + h, 8, fill=COLORS["panel"], outline=COLORS["line_soft"])
        self._text(x + 20, y + 24, self._t("settings_title"), COLORS["text"], "detail_title")

        self._text(x + 20, y + 84, self._t("interface_language"), COLORS["text_soft"], "section")
        lang_y = y + 118
        uk_active = self.interface_language == "uk"
        en_active = self.interface_language == "en"
        self._button(
            x + 20,
            lang_y,
            x + 150,
            lang_y + 36,
            "Українська",
            "set_language",
            "uk",
            fill=COLORS["blue"] if uk_active else COLORS["panel_soft"],
            active_fill=COLORS["blue_dark"] if uk_active else "#1c334d",
            radius=6,
        )
        self._button(
            x + 162,
            lang_y,
            x + 292,
            lang_y + 36,
            "English",
            "set_language",
            "en",
            fill=COLORS["blue"] if en_active else COLORS["panel_soft"],
            active_fill=COLORS["blue_dark"] if en_active else "#1c334d",
            radius=6,
        )

        self._text(x + 20, y + 188, self._t("theme"), COLORS["text_soft"], "section")
        theme_y = y + 222
        dark_active = self.theme_mode == "dark"
        light_active = self.theme_mode == "light"
        self._button(
            x + 20,
            theme_y,
            x + 150,
            theme_y + 36,
            self._t("dark_theme"),
            "set_theme",
            "dark",
            fill=COLORS["blue"] if dark_active else COLORS["panel_soft"],
            active_fill=COLORS["blue_dark"] if dark_active else "#1c334d",
            radius=6,
        )
        self._button(
            x + 162,
            theme_y,
            x + 292,
            theme_y + 36,
            self._t("light_theme"),
            "set_theme",
            "light",
            fill=COLORS["blue"] if light_active else COLORS["panel_soft"],
            active_fill=COLORS["blue_dark"] if light_active else "#1c334d",
            radius=6,
        )

    def _draw_cover(self, x: float, y: float, w: float, h: float, book: dict, *, small: bool) -> None:
        self._round_rect(x, y, x + w, y + h, 4, fill=book["cover_bg"], outline="#0b111a")
        self.canvas.create_rectangle(x + 4, y + 4, x + w - 4, y + h - 4, fill=book["cover_bg"], outline="#2a3040")

        accent = book["cover_accent"]
        if book["id"] == "1984":
            title_font = "cover_small" if small else "cover"
            self._text(x + w / 2, y + h * 0.23, "1984", accent, title_font, "center")
            self.canvas.create_oval(x + w * 0.24, y + h * 0.46, x + w * 0.76, y + h * 0.68, outline="#d9c47f", width=2)
            self.canvas.create_oval(x + w * 0.44, y + h * 0.53, x + w * 0.56, y + h * 0.62, fill="#101010", outline="")
            self._text(x + w / 2, y + h - 12, "ОРВЕЛЛ", "#d4b15f", "caption", "center")
        elif book["id"] == "hobbit":
            self.canvas.create_rectangle(x + 4, y + h * 0.58, x + w - 4, y + h - 4, fill="#17352c", outline="")
            self.canvas.create_arc(x + w * 0.08, y + h * 0.16, x + w * 0.92, y + h * 0.86, start=20, extent=140, outline=accent, width=2)
            self.canvas.create_polygon(
                x + w * 0.18,
                y + h - 6,
                x + w * 0.5,
                y + h * 0.42,
                x + w * 0.82,
                y + h - 6,
                fill="#2b5b42",
                outline="",
            )
            self._text(x + w / 2, y + 10, "ГОБІТ", "#f2d17b", "caption", "center")
        elif book["id"] == "sapiens":
            self.canvas.create_rectangle(x + 5, y + 5, x + w - 5, y + h - 5, fill="#f3eadc", outline="")
            self._text(x + w / 2, y + h * 0.22, "Sapiens", accent, "caption", "center")
            self.canvas.create_oval(x + w * 0.35, y + h * 0.43, x + w * 0.65, y + h * 0.62, outline="#4f382e", width=2)
            self._text(x + w / 2, y + h - 14, "ХАРАРІ", "#4f382e", "caption", "center")
        elif book["id"] == "think-grow":
            self.canvas.create_rectangle(x + 5, y + 5, x + w - 5, y + h - 5, fill="#17110b", outline="#59451d")
            self._text(x + w / 2, y + h * 0.28, "ДУМАЙ", accent, "caption", "center")
            self._text(x + w / 2, y + h * 0.48, "І БАГАТІЙ", accent, "caption", "center")
            self.canvas.create_line(x + 12, y + h - 16, x + w - 12, y + h - 16, fill=accent)
        else:
            self.canvas.create_rectangle(x + 5, y + 5, x + w - 5, y + h - 5, fill="#191613", outline="#5c4620")
            self._text(x + w / 2, y + h * 0.28, "КОРОТКА", accent, "caption", "center")
            self._text(x + w / 2, y + h * 0.45, "ІСТОРІЯ", accent, "caption", "center")
            self.canvas.create_oval(x + w * 0.28, y + h * 0.58, x + w * 0.72, y + h * 0.82, outline=accent)

        path = book.get("cover_image")
        if path:
            from pathlib import Path
            from PIL import Image, ImageTk
            image_path = Path(__file__).resolve().parent / path
            if image_path.is_file():
                with Image.open(image_path) as source:
                    image = source.convert("RGBA").resize(
                        (max(1, round(w)), max(1, round(h))), Image.Resampling.LANCZOS
                    )
                photo = ImageTk.PhotoImage(image)
                if not hasattr(self, "_cover_refs"):
                    self._cover_refs = []
                self._cover_refs.append(photo)
                self.canvas.create_image(x, y, image=photo, anchor="nw")
            

    def _trim(self, text: str, max_width: float, font: str = "body") -> str:
        text = str(text)
        if not text:
            return text
        font_obj = self.fonts[font]
        if font_obj.measure(text) <= max_width:
            return text
        ellipsis = "..."
        if font_obj.measure(ellipsis) >= max_width:
            return ellipsis
        trimmed = text
        while len(trimmed) > 1 and font_obj.measure(trimmed + ellipsis) > max_width:
            trimmed = trimmed[:-1]
        return trimmed.rstrip() + ellipsis

    def _text_fit(
        self,
        x: float,
        y: float,
        text: str,
        fill: str,
        font: str,
        anchor: str,
        max_width: float,
    ) -> int:
        return self._text(x, y, self._trim(text, max_width, font), fill, font, anchor)

    def _line_height(self, font: str) -> int:
        return self.fonts[font].metrics("linespace") + 2

    def _split_long_word(self, word: str, max_width: float, font: str) -> list[str]:
        if self.fonts[font].measure(word) <= max_width:
            return [word]

        chunks: list[str] = []
        chunk = ""
        for char in word:
            candidate = chunk + char
            if chunk and self.fonts[font].measure(candidate) > max_width:
                chunks.append(chunk)
                chunk = char
            else:
                chunk = candidate
        if chunk:
            chunks.append(chunk)
        return chunks

    def _wrap_text(self, text: str, max_width: float, font: str, max_lines: int | None = None) -> list[str]:
        words = str(text).split()
        if not words:
            return [""]

        lines: list[str] = []
        current = ""
        for word in words:
            for piece in self._split_long_word(word, max_width, font):
                candidate = f"{current} {piece}" if current else piece
                if current and self.fonts[font].measure(candidate) > max_width:
                    lines.append(current)
                    current = piece
                else:
                    current = candidate
        if current:
            lines.append(current)

        if max_lines is not None and len(lines) > max_lines:
            lines = lines[:max_lines]
            ellipsis = "..."
            if self.fonts[font].measure(lines[-1] + ellipsis) <= max_width:
                lines[-1] = lines[-1].rstrip() + ellipsis
            else:
                lines[-1] = self._trim(lines[-1], max_width, font)
        return lines

    def _text_block(
        self,
        x: float,
        y: float,
        text: str,
        fill: str,
        font: str,
        max_width: float,
        max_lines: int | None = None,
    ) -> float:
        lines = self._wrap_text(text, max_width, font, max_lines)
        line_height = self._line_height(font)
        self._text(x, y, "\n".join(lines), fill, font, "nw")
        return len(lines) * line_height


if __name__ == "__main__":
    BookDownloaderApp()
