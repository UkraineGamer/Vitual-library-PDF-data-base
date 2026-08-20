from tkinter import *
from tkinter import ttk
import tkinter as tk
from tkinter import filedialog


root = Tk()
root.title("Virtual Library")
root.geometry("900x600")
root.withdraw()  # приховати головне вікно

file_path = filedialog.askopenfilename()

print(file_path)

# app = App()
# app.mainloop()
# root.mainloop()