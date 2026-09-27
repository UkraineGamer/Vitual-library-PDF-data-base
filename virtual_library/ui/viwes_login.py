import sys
from pathlib import Path
import tkinter as tk

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from virtual_library.ui import BookDownloaderApp

root = tk.Tk()
root.geometry("1000x800")
root.title("Login")

def open_library():
    root.destroy()              # закрити це вікно
    BookDownloaderApp().run()   # відкрити інший інтерфейс


btn = tk.Button(root, text="Login", command=open_library)
btn.pack()

root.mainloop()