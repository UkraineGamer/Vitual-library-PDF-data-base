# Virtual Library PDF Database

Запуск застосунку:

```powershell
python main.py
```

Структура проєкту:

```
virtual_library/
├── config.py              # кольори, переклади та UI-типи
├── settings.py            # змінні середовища
├── data/
│   └── catalog.py          # вбудований каталог та історія завантажень
├── services/
│   └── book_search.py     # запити до Open Library і вибір файлу
└── ui/
    ├── app.py             # стан, події та запуск вікна
    ├── components.py      # базові елементи Canvas
    └── views.py           # екрани та панелі інтерфейсу
main.py                    # точка запуску
```
