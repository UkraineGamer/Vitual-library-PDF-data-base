import tkinter as tk
from tkinter import font as tkfont


COLORS = {
    "app": "#07121f",
    "sidebar": "#0a1624",
    "sidebar_active": "#132742",
    "panel": "#0f1a28",
    "panel_alt": "#132234",
    "panel_soft": "#17283d",
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


BOOKS = [
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
    ("⌂", "Головна"),
    ("⌕", "Пошук книг"),
    ("⇩", "Завантаження"),
    ("◷", "Історія"),
    ("▥", "Бібліотека"),
    ("♡", "Обране"),
    ("⚙", "Налаштування"),
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
        self.bookmarked = True
        self.favorite = False
        self.filter_open = False
        self.placeholder_active = True

        self.search_entry = tk.Entry(
            self.root,
            bd=0,
            relief=tk.FLAT,
            bg="#0b1624",
            fg=COLORS["text_muted"],
            insertbackground=COLORS["text"],
            font=self.fonts["body"],
        )
        self.search_entry.insert(0, "Пошук книг за назвою, автором або ISBN...")
        self.search_entry.bind("<FocusIn>", self._on_entry_focus_in)
        self.search_entry.bind("<FocusOut>", self._on_entry_focus_out)
        self.search_entry.bind("<KeyRelease>", self._on_search_change)
        self.search_entry.bind("<Return>", lambda _event: self.draw())

        self.canvas.bind("<Configure>", lambda _event: self.draw())
        self.canvas.bind("<Button-1>", self._on_click)
        self.canvas.bind("<Motion>", self._on_motion)
        self.canvas.bind("<Leave>", self._on_leave)

        self.draw()
        self.root.mainloop()

    def _build_fonts(self) -> dict[str, tkfont.Font]:
        return {
            "brand": tkfont.Font(family="Segoe UI", size=10, weight="bold"),
            "nav": tkfont.Font(family="Segoe UI", size=10),
            "body": tkfont.Font(family="Segoe UI", size=10),
            "body_small": tkfont.Font(family="Segoe UI", size=9),
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
            self._text(x1 + 14, center_y, icon, text_fill, "body", "w")
            self._text(x1 + 36, center_y, label, text_fill, font, "w")
        else:
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
        for book in BOOKS:
            if book["id"] == book_id:
                return book
        return BOOKS[0]

    def _query(self) -> str:
        if self.placeholder_active:
            return ""
        return self.search_entry.get().strip().casefold()

    def _visible_books(self) -> list[dict]:
        query = self._query()
        visible = []
        for book in BOOKS:
            if self.active_category not in ("Усі", "Більше⌄") and self.active_category not in book["categories"]:
                continue
            haystack = " ".join(
                [
                    book["title"],
                    book["author"],
                    book["meta"],
                    book["isbn"],
                ]
            ).casefold()
            if query and query not in haystack:
                continue
            visible.append(book)
        return visible

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
            self.search_entry.insert(0, "Пошук книг за назвою, автором або ISBN...")
            self.draw()

    def _on_search_change(self, _event: tk.Event) -> None:
        if not self.placeholder_active:
            self.draw()

    def _on_click(self, event: tk.Event) -> None:
        for button in reversed(self.buttons):
            if button["x1"] <= event.x <= button["x2"] and button["y1"] <= event.y <= button["y2"]:
                self._handle_action(button["action"], button["payload"])
                return

    def _on_motion(self, event: tk.Event) -> None:
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
            self.active_nav = payload
        elif action == "category" and payload:
            self.active_category = payload
            visible = self._visible_books()
            if visible and self.selected_book_id not in {book["id"] for book in visible}:
                self.selected_book_id = visible[0]["id"]
        elif action == "select_book" and payload:
            self.selected_book_id = payload
        elif action == "search":
            self.draw()
            return
        elif action == "filter":
            self.filter_open = not self.filter_open
        elif action == "bookmark":
            self.bookmarked = not self.bookmarked
        elif action == "favorite":
            self.favorite = not self.favorite
        elif action == "download" and payload:
            self._start_download(payload)
        elif action == "remove_download" and payload:
            DOWNLOADS[:] = [item for item in DOWNLOADS if item["book_id"] != payload]
        self.draw()

    def _start_download(self, book_id: str) -> None:
        book = self._book_by_id(book_id)
        for item in DOWNLOADS:
            if item["book_id"] == book_id:
                item["status"] = "Завершено"
                item["date"] = "Щойно"
                item["size"] = book["size"]
                item["progress"] = 100
                return
        DOWNLOADS.insert(
            0,
            {
                "book_id": book_id,
                "status": "Завершено",
                "date": "Щойно",
                "size": book["size"],
                "progress": 100,
            },
        )

    def draw(self) -> None:
        width = max(self.canvas.winfo_width(), 1060)
        height = max(self.canvas.winfo_height(), 700)
        self.canvas.delete("all")
        self.buttons = []

        self._round_rect(1, 1, width - 2, height - 2, 10, fill=COLORS["app"], outline="#0f2538")
        self._draw_sidebar(height)

        content_x = 215
        content_y = 22
        content_w = width - content_x - 14
        right_w = 398 if content_w > 890 else 350
        gap = 12
        right_x = width - right_w - 14
        left_w = right_x - content_x - gap

        self._draw_search(content_x + 10, content_y, left_w - 10, right_x, right_w)
        panel_top = 116
        downloads_h = 226
        bottom_margin = 14
        results_h = max(342, height - panel_top - downloads_h - 24)
        self._draw_results(content_x + 10, panel_top, left_w - 10, results_h)
        self._draw_downloads(content_x + 10, panel_top + results_h + 10, left_w - 10, downloads_h)
        self._draw_details(right_x, panel_top, right_w, height - panel_top - bottom_margin)

    def _draw_sidebar(self, height: float) -> None:
        sidebar_w = 195
        self.canvas.create_rectangle(0, 0, sidebar_w, height, fill=COLORS["sidebar"], outline="")
        self.canvas.create_line(sidebar_w, 0, sidebar_w, height, fill="#0f2438")

        self._round_rect(17, 19, 34, 36, 4, fill=COLORS["blue"], outline="")
        self._text(25.5, 27.5, "▥", "#d9efff", "caption", "center")
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
            self._text(44, y + row_h / 2, label, text_fill, "nav", "w")
            self.buttons.append(
                {"x1": 9, "y1": y, "x2": sidebar_w - 10, "y2": y + row_h, "action": "nav", "payload": label}
            )
            y += 42

        storage_y = height - 64
        self._text(21, storage_y, "Сховище", COLORS["text_soft"], "body_small")
        self._round_rect(21, storage_y + 18, 174, storage_y + 23, 3, fill="#15253a", outline="")
        self._round_rect(21, storage_y + 18, 88, storage_y + 23, 3, fill=COLORS["blue"], outline="")
        self._text(21, storage_y + 32, "18.4 ГБ / 50 ГБ", COLORS["text_soft"], "body_small")

    def _draw_search(self, x: float, y: float, left_w: float, right_x: float, right_w: float) -> None:
        search_w = min(620, max(420, left_w - 10))
        self._round_rect(x, y, x + search_w, y + 36, 7, fill="#0b1624", outline="#1c3046")
        self.search_entry.place(x=x + 16, y=y + 9, width=search_w - 126, height=20)
        self._button(
            x + search_w - 82,
            y + 1,
            x + search_w,
            y + 35,
            "Пошук",
            "search",
            fill=COLORS["blue"],
            active_fill=COLORS["blue_dark"],
            radius=7,
            icon="⌕",
        )

        chip_x = x
        chip_y = y + 51
        for category in CATEGORIES:
            label = category
            chip_w = max(32, self.fonts["body_small"].measure(label) + 24)
            if chip_x + chip_w > x + left_w:
                break
            active = self.active_category == category
            fill = COLORS["blue"] if active else COLORS["panel_alt"]
            text_fill = COLORS["text"] if active else COLORS["text_soft"]
            self._button(
                chip_x,
                chip_y,
                chip_x + chip_w,
                chip_y + 27,
                label,
                "category",
                category,
                fill=fill,
                active_fill=COLORS["blue_dark"] if active else COLORS["panel_soft"],
                text_fill=text_fill,
                radius=7,
                font="body_small",
            )
            chip_x += chip_w + 8

        filter_label = "Фільтри" if not self.filter_open else "Фільтри: відкрито"
        self._button(
            right_x + 20,
            y + 41,
            right_x + min(150, right_w - 16),
            y + 75,
            filter_label,
            "filter",
            fill=COLORS["panel_alt"],
            active_fill=COLORS["panel_soft"],
            radius=7,
            icon="≡",
        )

    def _draw_results(self, x: float, y: float, w: float, h: float) -> None:
        self._round_rect(x, y, x + w, y + h, 8, fill=COLORS["panel"], outline=COLORS["line_soft"])
        self._text(x + 14, y + 14, "Результати пошуку", COLORS["text"], "section")

        books = self._visible_books()
        selected_ids = {book["id"] for book in books}
        if books and self.selected_book_id not in selected_ids:
            self.selected_book_id = books[0]["id"]

        row_x = x + 14
        row_y = y + 40
        row_w = w - 28
        row_h = 87
        max_rows = int((h - 50) // row_h)
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

        for index, book in enumerate(books[:max_rows]):
            top = row_y + index * row_h
            active = book["id"] == self.selected_book_id
            fill = COLORS["panel_alt"] if active else COLORS["panel"]
            if active:
                self._round_rect(row_x, top, row_x + row_w, top + row_h - 9, 6, fill=fill, outline="")
            else:
                self.canvas.create_line(row_x, top + row_h - 8, row_x + row_w, top + row_h - 8, fill=COLORS["line_soft"])
            self.buttons.append(
                {
                    "x1": row_x,
                    "y1": top,
                    "x2": row_x + row_w,
                    "y2": top + row_h - 9,
                    "action": "select_book",
                    "payload": book["id"],
                }
            )
            self._draw_cover(row_x + 8, top + 9, 52, 70, book, small=True)

            text_x = row_x + 74
            self._text(text_x, top + 11, self._trim(book["title"], 36), COLORS["text"], "title")
            self._text(text_x, top + 35, book["author"], COLORS["text_soft"], "body_small")
            meta = f"{book['meta']}  •  {book['pages']} стор."
            self._text(text_x, top + 56, meta, COLORS["text_muted"], "body_small")
            self._text(text_x, top + 72, f"ISBN: {book['isbn']}", COLORS["text_muted"], "caption")

            btn_w = 112
            btn_x = row_x + row_w - btn_w - 22
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
            self._text(btn_x + 20, top + 66, f"{book['format']}  •  {book['size']}", COLORS["text_muted"], "caption")

    def _draw_downloads(self, x: float, y: float, w: float, h: float) -> None:
        self._round_rect(x, y, x + w, y + h, 8, fill=COLORS["panel"], outline=COLORS["line_soft"])
        self._text(x + 14, y + 14, "Історія завантажень", COLORS["text"], "section")
        self._text(x + w - 14, y + 15, "Переглянути всю історію", COLORS["blue"], "body_small", "ne")

        row_y = y + 38
        row_h = 44
        compact = w < 610
        for index, item in enumerate(DOWNLOADS[:4]):
            book = self._book_by_id(item["book_id"])
            top = row_y + index * row_h
            if index > 0:
                self.canvas.create_line(x + 14, top - 3, x + w - 14, top - 3, fill=COLORS["line_soft"])

            self._draw_cover(x + 22, top, 28, 38, book, small=True)
            title_limit = 22 if compact else 26
            self._text(x + 61, top + 2, self._trim(book["title"], title_limit), COLORS["text"], "body_small")
            self._text(x + 61, top + 20, book["author"], COLORS["text_muted"], "caption")

            status_x = x + w - 220 if compact else x + max(330, w * 0.52)
            is_done = item["progress"] >= 100
            self._text(status_x, top + 16, "●", COLORS["green"] if is_done else COLORS["blue"], "body_small", "center")
            self._text(
                status_x + 14,
                top + 8,
                item["status"],
                COLORS["text_soft"] if is_done else COLORS["blue"],
                "caption",
            )
            if not is_done:
                self._round_rect(status_x + 14, top + 27, status_x + 106, top + 31, 3, fill="#132741", outline="")
                progress_w = 92 * item["progress"] / 100
                self._round_rect(status_x + 14, top + 27, status_x + 14 + progress_w, top + 31, 3, fill=COLORS["blue"], outline="")
                self._text(status_x + 112, top + 8, f"{item['progress']}%", COLORS["text_muted"], "caption")

            if compact:
                self._text(x + w - 92, top + 12, item["size"], COLORS["text_muted"], "caption", "e")
            else:
                date_x = x + max(430, w * 0.67)
                self._text(date_x, top + 12, item["date"], COLORS["text_muted"], "caption")
                self._text(x + w - 122, top + 12, item["size"], COLORS["text_muted"], "caption", "e")
            self._text(x + w - 58, top + 16, "□", COLORS["text_muted"], "body_small", "center")
            pause_or_close = "Ⅱ" if not is_done else "×"
            self._text(x + w - 25, top + 16, pause_or_close, COLORS["text_muted"], "body", "center")
            self.buttons.append(
                {
                    "x1": x + w - 42,
                    "y1": top,
                    "x2": x + w - 10,
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
        self._text(info_x, cover_y + 6, self._trim(book["title"], 24), COLORS["text"], "detail_title")
        detail_lines = [
            book["author"],
            book["meta"],
            f"Мова: {book['language']}",
            f"Формат: {book['format']}",
            f"Розмір: {book['size']}",
            f"Сторінок: {book['pages']}",
            f"ISBN: {book['isbn']}",
        ]
        for i, line in enumerate(detail_lines):
            self._text(info_x, cover_y + 48 + i * 22, line, COLORS["text_soft"], "body_small")

        self._text(info_x, cover_y + 164, "★★★★★", COLORS["yellow"], "body")
        self._text(info_x, cover_y + 186, f"{book['rating']} ({book['reviews']} оцінок)", COLORS["text_soft"], "body_small")

        action_y = cover_y + 228
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
            "▣" if self.bookmarked else "□",
            "bookmark",
            fill=COLORS["panel_soft"],
            active_fill="#1c334d",
            radius=6,
        )
        self._button(
            x + w - 70,
            action_y,
            x + w - 16,
            action_y + 38,
            "♥" if self.favorite else "♡",
            "favorite",
            fill=COLORS["panel_soft"],
            active_fill="#1c334d",
            radius=6,
            text_fill=COLORS["danger"] if self.favorite else COLORS["text_soft"],
        )

        desc_y = action_y + 66
        self._text(x + 20, desc_y, "Опис", COLORS["text"], "section")
        self._text(x + 20, desc_y + 34, book["description"], COLORS["text_soft"], "body_small", width=w - 40)
        self._text(x + 20, desc_y + 100, "Показати більше  ⌄", COLORS["blue"], "body_small")

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
        for i, (label, value) in enumerate(rows):
            row_y = info_y + 42 + i * 26
            self._text(x + 20, row_y, label, COLORS["text_muted"], "body_small")
            self._text(x + w - 20, row_y, value, COLORS["text_soft"], "body_small", "ne")

        if self.filter_open:
            self._draw_filter_popover(x - 170, y + 76)

    def _draw_filter_popover(self, x: float, y: float) -> None:
        self._round_rect(x, y, x + 150, y + 116, 8, fill="#0d1827", outline=COLORS["line"])
        self._text(x + 12, y + 12, "Швидкі фільтри", COLORS["text"], "section")
        self._text(x + 12, y + 42, "EPUB", COLORS["text_soft"], "body_small")
        self._text(x + 12, y + 65, "Українська мова", COLORS["text_soft"], "body_small")
        self._text(x + 12, y + 88, "4+ зірки", COLORS["text_soft"], "body_small")

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

    def _trim(self, text: str, limit: int) -> str:
        if len(text) <= limit:
            return text
        return text[: max(0, limit - 3)].rstrip() + "..."


if __name__ == "__main__":
    BookDownloaderApp()
