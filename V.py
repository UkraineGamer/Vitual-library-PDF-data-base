from tkinter import *
from tkinter import ttk
import tkinter as tk


root = Tk()
root.title("Virtual Library")
root.geometry("900x600")

class App(tk.Tk):
    def __init__(self):
        super().__init__()


        self.title("Virtual Library")
        self.geometry("900x600")

        self.screen1 = HomePage(self)
        self.screen2 = SettingsPage(self)

        self.show_screen(self.HomePage)

    def show_screen(self, screen):
        for widget in self.winfo_children():
            widget.pack_forget()

        screen.pack(fill="both", expand=True)

class HomePage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        tk.Button(
            self,
            text="Home",
        ).pack(anchor="nw", padx=10, pady=15)
        tk.Button(
            text="Search"
        )
        tk.Button(
            text="Download"
        )
        tk.Button(
            text="History"
        )
        tk.Button(
            text="Library"
        )
        tk.Button(
            text="Lovely"
        )
        tk.Button(
            self,
            text="Settings",
            command=lambda: app.show_screen(SettingsPage)
        )

class SettingsPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        tk.Button(
            self,
            text="Exit",
            command=lambda: app.show_screen(self.HomePage)
        )

# btn = ttk.Button(text="Home")
# btn.pack(anchor="nw", padx=10, pady=15)
# btn = ttk.Button(text="Search")
# btn.pack(anchor="nw", padx=10, pady=5)
# btn = ttk.Button(text="Download")
# btn.pack(anchor="nw", padx=10, pady=5)
# btn = ttk.Button(text="History")
# btn.pack(anchor="nw", padx=10, pady=5)
# btn = ttk.Button(text="Library")
# btn.pack(anchor="nw", padx=10, pady=5)
# btn = ttk.Button(text="Lovely")
# btn.pack(anchor="nw", padx=10, pady=5)
# btn = ttk.Button(text="Settings")
# btn.pack(anchor="nw", padx=10, pady=5)

app = App()
app.mainloop()
# root.mainloop()