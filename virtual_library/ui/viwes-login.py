import tkinter as tk
from virtual_library.ui import BookDownloaderApp

root = tk.Tk()
root.geometry("1000x800")
root.title("Login")

def click_button():
    root.destroy()
    BookDownloaderApp().run() 

btn = tk.Button(root, text="Login", command=click_button)
btn.pack()

root.mainloop()