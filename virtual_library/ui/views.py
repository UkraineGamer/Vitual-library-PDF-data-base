from virtual_library.config import COLORS
from virtual_library.data import BOOKS, DOWNLOADS, SIDEBAR_ITEMS


class AppViewsMixin:

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
        return 20 + max(27, self._line_height("body_small") + 10) + 14

    def _draw_search_bar(self, x: float, y: float, left_w: float) -> None:
        search_w = left_w
        search_label = self._t("search")
        search_button_w = 36 + self._measure(search_label, "button") + 14
        search_h = max(44, self._line_height("body") + 22)
        self._round_rect(x, y, x + search_w, y + search_h, 7, fill=COLORS["input_bg"], outline=COLORS["input_line"])
        self.canvas.coords(self._search_window, x + 12, y + 8)
        self.canvas.itemconfigure(self._search_window, width=max(1, search_w - search_button_w - 24), height=search_h - 16)
        self._button(
            x + search_w - search_button_w,
            y + 1,
            x + search_w,
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
        filter_h = max(34, self._line_height("button") + 12)
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
        left = geom["viewport_x"]
        right = left + geom["viewport_w"]
        y1 = geom["chip_y"]
        y2 = y1 + geom["chip_h"] + 1
        self.canvas.create_rectangle(geom["x"], y1, left, y2, fill=COLORS["panel"], outline="")
        self.canvas.create_rectangle(right, y1, geom["x"] + geom["w"], y2, fill=COLORS["panel"], outline="")

    def _draw_category_container(self, x: float, y: float, w: float) -> float:
        pad_x = 12
        pad_y = 10
        chip_h = max(27, self._line_height("body_small") + 10)
        scroll_h = 6
        container_h = self._category_container_height()

        self._round_rect(x, y, x + w, y + container_h, 8, fill=COLORS["panel"], outline=COLORS["line_soft"])

        viewport_x = x + pad_x
        viewport_w = max(1, w - pad_x * 2 - 150)
        chip_y = y + pad_y

        chips, total_w = self._category_chips_metrics()
        max_scroll = max(0, int(total_w - viewport_w))
        self.category_scroll = max(0, min(self.category_scroll, max_scroll))
        has_scroll = max_scroll > 0
        self.category_scroll_bounds = (viewport_x, y, viewport_x + viewport_w, y + container_h, max_scroll)
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
                    max(chip_x, viewport_x),
                    chip_y,
                    min(chip_right, viewport_x + viewport_w),
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
            thumb_w = min(track_w, max(28, track_w * viewport_w / total_w))
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
        self._text_fit(x + 14, y + 14, "Пошук…" if self._search_pending else "Результати пошуку", COLORS["text"], "section", "nw", w - 28)

        books = self._visible_books()
        selected_ids = {book["id"] for book in books}
        if books and self.selected_book_id not in selected_ids:
            self.selected_book_id = books[0]["id"]

        row_x = x + 14
        row_y = y + 40
        row_h = max(96, self._line_height("title") + 2 * self._line_height("body_small") + self._line_height("caption") + 20)
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
            self._text_fit(
                x + w / 2,
                y + h / 2 + 24,
                "Спробуйте іншу назву, автора або ISBN.",
                COLORS["text_muted"],
                "body_small",
                "center",
                w - 28,
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
            btn_w = self._measure("Завантажити", "button") + 50 if row_w >= 420 else 36
            btn_x = row_x + row_w - btn_w - 8
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
            text_max_w = max(1, btn_x - text_x - 8)
            text_y = top + 6
            for value, font, color in ((book["title"], "title", "text"), (book["author"], "body_small", "text_soft"),
                                       (f"{book['meta']} • {book['pages']} стор.", "body_small", "text_muted"),
                                       (f"ISBN: {book['isbn']}", "caption", "text_muted")):
                self._text_fit(text_x, text_y, value, COLORS[color], font, "nw", text_max_w)
                text_y += self._line_height(font)

            self._button(
                btn_x,
                top + 18,
                btn_x + btn_w,
                top + 52,
                "Завантажити" if btn_w > 36 else "⇩",
                "download",
                book["id"],
                fill=COLORS["panel_soft"],
                active_fill="#1c334d",
                radius=6,
                icon="⇩" if btn_w > 36 else None,
            )
            self._text_fit(
                btn_x + (btn_w / 2),
                top + 66,
                f"{book['format']} • {book['size']}" if btn_w > 36 else "",
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
            thumb_h = min(track_h, max(28, track_h * max_rows / len(books)))
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

    def _download_card_height(self):
        return 2 * self._line_height("body_small") + 3 * self._line_height("caption") + 22

    def _draw_downloads(self, x, y, w, h):
        self._round_rect(x, y, x + w, y + h, 8, fill=COLORS["panel"], outline=COLORS["line_soft"])
        self._text_fit(x + 14, y + 14, self._t("download_history"), COLORS["text"], "section", "nw", w - 28)
        self._button(x + 14, y + h - 40, x + w - 14, y + h - 8, self._t("view_all_history"), "show_history")
        count = max(0, int((h - 88) // self._download_card_height()))
        self._draw_download_cards(x + 14, y + 40, w - 28, DOWNLOADS[:count])

    def _draw_download_cards(self, x, y, w, items):
        row_h = self._download_card_height()
        for index, item in enumerate(items):
            top = y + index * row_h
            book = self._book_by_id(item["book_id"])
            text_x = x + 44
            text_w = max(1, w - 92)
            self._draw_cover(x + 4, top + 6, 28, 40, book, small=True)
            self._text_block(text_x, top + 4, book["title"], COLORS["text"], "body_small", text_w, max_lines=2)
            author_y = top + 4 + 2 * self._line_height("body_small")
            self._text_fit(text_x, author_y, book["author"], COLORS["text_muted"], "caption", "nw", text_w)
            status = f"{item['status']} • {item['size']} • {item.get('date', '')}"
            if item["progress"] < 100:
                status += f" • {item['progress']}%"
            self._text_block(text_x, author_y + self._line_height("caption"), status, COLORS["text_soft"], "caption", text_w, max_lines=2)
            self._button(x + w - 36, top + 6, x + w, top + 40, "×", "remove_download", book["id"])
            self.canvas.create_line(x, top + row_h - 4, x + w, top + row_h - 4, fill=COLORS["line_soft"])

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
        row_h = max(54, self._line_height("body_small") + self._line_height("caption") + 14)
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

    def _draw_details(self, x, y, w, h):
        book = self._book_by_id(self.selected_book_id)
        title_lines = self._wrap_text(book["title"], w - 40, "detail_title", max_lines=2)
        cover_y = y + 20 + len(title_lines) * self._line_height("detail_title") + 16
        cover_w = min(120, w * 0.29)
        cover_h = cover_w * 1.45
        detail_x = x + 32 + cover_w
        detail_w = x + w - 20 - detail_x
        detail_lines = [book["author"], book["meta"], f"Мова: {book['language']}", f"Формат: {book['format']}",
                        f"Розмір: {book['size']}", f"Сторінок: {book['pages']}", f"ISBN: {book['isbn']}"]
        detail_gap = self._line_height("body_detail")
        rating_y = cover_y + len(detail_lines) * detail_gap + 12
        action_y = max(cover_y + cover_h, rating_y + 2 * self._line_height("body_small")) + 20
        button_h = max(38, self._line_height("button") + 16)
        desc_y = action_y + button_h + 24
        desc_text_y = desc_y + self._line_height("section") + 12
        desc_lines = self._wrap_text(book["description"], w - 40, "body_small", max_lines=4 if self.description_expanded else 1)
        more_y = desc_text_y + len(desc_lines) * self._line_height("body_small") + 16
        info_y = more_y + button_h + 24
        rows = [("Формат", book["format"]), ("Розмір файлу", book["size"]),
                ("Дата публікації", book["date"]), ("Видавництво", book["publisher"])]
        item = next((item for item in DOWNLOADS if item["book_id"] == book["id"]), None)
        if item and item.get("file_path"):
            rows.append(("Шлях до файлу", item["file_path"]))
        row_h = self._line_height("body_small") * 2 + 8
        bottom = info_y + self._line_height("section") + 16 + len(rows) * row_h + 20
        self._round_rect(x, y, x + w, max(y + h, bottom), 8, fill=COLORS["panel"], outline=COLORS["line_soft"])
        self._text(x + 20, y + 20, "\n".join(title_lines), COLORS["text"], "detail_title")
        self._draw_cover(x + 20, cover_y, cover_w, cover_h, book, small=False)
        for index, line in enumerate(detail_lines):
            self._text_fit(detail_x, cover_y + index * detail_gap, line, COLORS["text_soft"], "body_detail", "nw", detail_w)
        self._text_fit(detail_x, rating_y, "★★★★★", COLORS["yellow"], "body_small", "nw", detail_w)
        self._text_fit(detail_x, rating_y + self._line_height("body_small"), f"{book['rating']} ({book['reviews']} оцінок)", COLORS["text_soft"], "body_small", "nw", detail_w)
        self._button(x + 20, action_y, x + w - 120, action_y + button_h, "Завантажити", "download", book["id"], fill=COLORS["blue"], active_fill=COLORS["blue_dark"], icon="⇩")
        self._button(x + w - 108, action_y, x + w - 68, action_y + button_h, "▣" if book["id"] in self.bookmarks else "□", "bookmark", book["id"])
        self._button(x + w - 60, action_y, x + w - 20, action_y + button_h, "♥" if book["id"] in self.favorites else "♡", "favorite", book["id"])
        self._text(x + 20, desc_y, "Опис", COLORS["text"], "section")
        self._text(x + 20, desc_text_y, "\n".join(desc_lines), COLORS["text_soft"], "body_small")
        self._button(x + 20, more_y, x + w - 20, more_y + button_h, "Показати менше ⌃" if self.description_expanded else "Показати більше ⌄", "toggle_description")
        self._text_fit(x + 20, info_y, "Інформація про файл", COLORS["text"], "section", "nw", w - 40)
        label_w = (w - 52) * 0.44
        for index, (label, value) in enumerate(rows):
            row_y = info_y + self._line_height("section") + 16 + index * row_h
            self._text_block(x + 20, row_y, label, COLORS["text_muted"], "body_small", label_w, max_lines=2)
            self._text_block(x + 32 + label_w, row_y, value, COLORS["text_soft"], "body_small", w - 52 - label_w, max_lines=2)

    def _draw_filter_popover(self, x: float, y: float) -> None:
        self._round_rect(x, y, x + 150, y + 116, 8, fill=COLORS["panel"], outline=COLORS["line"])
        self._text_fit(x + 12, y + 12, "Швидкі фільтри", COLORS["text"], "section", "nw", 126)
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

    def _draw_full_history(self, x, y, w, h):
        narrow = w < 760
        row_h = self._download_card_height() if narrow else max(54, self._line_height("body_small") + self._line_height("caption") + 14)
        h = max(h, 90 + len(DOWNLOADS) * row_h)
        self._round_rect(x, y, x + w, y + h, 8, fill=COLORS["panel"], outline=COLORS["line_soft"])
        self._text_fit(x + 14, y + 14, self._t("full_history"), COLORS["text"], "section", "nw", w - 28)
        if narrow:
            self._draw_download_cards(x + 14, y + 48, w - 28, DOWNLOADS)
        else:
            self._draw_download_table_header(x + 14, y + 40, w - 28)
            self._draw_download_rows(x + 14, y + 70, w - 28, h - 84, DOWNLOADS, table_mode=True)

    def _draw_settings(self, x, y, w, h):
        self._round_rect(x, y, x + w, y + h, 8, fill=COLORS["panel"], outline=COLORS["line_soft"])
        self._text_fit(x + 20, y + 24, self._t("settings_title"), COLORS["text"], "detail_title", "nw", w - 40)
        sections = [
            ("interface_language", "set_language", self.interface_language, [("uk", "Українська"), ("en", "English")]),
            ("theme", "set_theme", self.theme_mode, [("dark", self._t("dark_theme")), ("light", self._t("light_theme"))]),
            ("font_size", "set_font_size", self.font_size, [(key, self._t(key)) for key in ("small", "medium", "large")]),
        ]
        top = y + 90
        for title, action, active, options in sections:
            self._text_fit(x + 20, top, self._t(title), COLORS["text_soft"], "section", "nw", w - 40)
            button_y = top + self._line_height("section") + 16
            button_h = max(38, self._line_height("button") + 16)
            button_w = (w - 40 - 8 * (len(options) - 1)) / len(options)
            for index, (value, label) in enumerate(options):
                left = x + 20 + index * (button_w + 8)
                self._button(left, button_y, left + button_w, button_y + button_h, label, action, value,
                             fill=COLORS["blue"] if value == active else COLORS["panel_soft"], active_fill=COLORS["blue_dark"])
            top = button_y + button_h + 28
