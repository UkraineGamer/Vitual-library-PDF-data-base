from typing import Literal

TextAnchor = Literal["nw", "n", "ne", "w", "center", "e", "sw", "s", "se"]
TextJustify = Literal["left", "center", "right"]

COLORS = {
    "app": "#07121f", "sidebar": "#0a1624", "sidebar_active": "#132742",
    "panel": "#0f1a28", "panel_alt": "#132234", "panel_soft": "#17283d",
    "input_bg": "#0b1624", "input_line": "#1c3046", "line": "#203246",
    "line_soft": "#172638", "text": "#e8eef8", "text_soft": "#a8b4c6",
    "text_muted": "#748195", "blue": "#0a84ff", "blue_dark": "#086ed3",
    "green": "#35c46a", "yellow": "#ffcc33", "danger": "#e76f6f",
}

DARK_COLORS = COLORS.copy()
LIGHT_COLORS = {
    "app": "#f4f7fb", "sidebar": "#eef3f8", "sidebar_active": "#dbeafe",
    "panel": "#ffffff", "panel_alt": "#f1f5f9", "panel_soft": "#e5edf7",
    "input_bg": "#ffffff", "input_line": "#cbd5e1", "line": "#c7d2df",
    "line_soft": "#dbe3ec", "text": "#172033", "text_soft": "#435369",
    "text_muted": "#6f7d91", "blue": "#0a84ff", "blue_dark": "#086ed3",
    "green": "#238b52", "yellow": "#c28700", "danger": "#d84f4f",
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
        "font_size": "Розмір шрифту",
        "small": "Малий",
        "medium": "Середній",
        "large": "Великий",
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
        "font_size": "Font size",
        "small": "Small",
        "medium": "Medium",
        "large": "Large",
        "nav_home": "Home",
        "nav_search": "Book search",
        "nav_downloads": "Downloads",
        "nav_history": "History",
        "nav_library": "Library",
        "nav_favorites": "Favorites",
        "nav_settings": "Settings",
    },
}
