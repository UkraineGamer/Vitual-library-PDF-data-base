from cProfile import label
import sys
from pathlib import Path
import tkinter as tk
from virtual_library.config import COLORS


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from virtual_library.ui import BookDownloaderApp

class RegisterWindow:
    root = tk.Tk()
    root.geometry("700x800")
    root.title("Register")

    root.configure(bg="#07121f")



    def click_button(self):
        self.root.destroy()
        BookDownloaderApp().run() 

    btn = tk.Button(root, text="Enter", command=click_button)
    btn.pack(anchor="s")

    label = tk.Label(text = "Create your account", font =("Arial", 15))
    label.pack()

    #name
    tk.Entry().pack(anchor="n", pady= 10)



    #@
    tk.Entry().pack(anchor="n", pady= 10)

    #password
    tk.Entry().pack(anchor="n", pady= 10)

    def open_login_window(self):
        self.root.destroy()
        login_window = tk.Tk()
        login_window.title("Log in")
        login_window.geometry("700x800")

    btn = tk.Button(text="Login", command=open_login_window)
    btn.pack(anchor='s', expand=1)





    root.mainloop()