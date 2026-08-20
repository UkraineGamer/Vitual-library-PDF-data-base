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


from virtual_library.config import COLORS, DARK_COLORS, LIGHT_COLORS, TextAnchor, TextJustify, UI_STRINGS
from virtual_library.services import BookSearch



