"""Compatibility wrapper for the shared file picker."""
from virtual_library.services import BookSearch


class Url_path:
    def __init__(self):
        self.fi = ""

    def save_path(self, parent=None):
        self.fi = BookSearch().get_file_path(parent)
        return self.fi


if __name__ == "__main__":
    import tkinter as tk
    root = tk.Tk()
    root.withdraw()
    try:
        print(Url_path().save_path(root))
    finally:
        root.destroy()
