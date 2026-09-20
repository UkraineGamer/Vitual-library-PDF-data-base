import tkinter as tk
from tkinter import messagebox

from pymongo.errors import PyMongoError

from login_register.register import UserRegister


class RegisterWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title('Library account')
        self.root.geometry('400x260')
        self.authenticated = False
        tk.Label(self.root, text='Username').pack(pady=(16, 0))
        self.username = tk.Entry(self.root)
        self.username.pack()
        tk.Label(self.root, text='Password').pack(pady=(12, 0))
        self.password = tk.Entry(self.root, show='*')
        self.password.pack()
        tk.Button(self.root, text='Register', command=self.register).pack(pady=(12, 0))
        tk.Button(self.root, text='Login', command=self.login).pack()

    def _submit(self, register: bool):
        service = None
        try:
            UserRegister._credentials(self.username.get(), self.password.get())
            service = UserRegister()
            if register:
                success = service.register_user(self.username.get(), self.password.get())
                messagebox.showinfo('Registration', 'Account created. You can log in.' if success else 'Username already exists.', parent=self.root)
            elif service.login_user(self.username.get(), self.password.get()):
                self.authenticated = True
                self.root.destroy()
            else:
                messagebox.showerror('Login', 'Invalid username or password.', parent=self.root)
        except (ValueError, RuntimeError, PyMongoError) as error:
            message = str(error) if isinstance(error, (ValueError, RuntimeError)) else 'Cannot access the account database. Check the connection settings.'
            messagebox.showerror('Account', message, parent=self.root)
        finally:
            if service is not None:
                service.close()

    def register(self):
        self._submit(register=True)

    def login(self):
        self._submit(register=False)

    def run(self):
        self.root.mainloop()
        if self.authenticated:
            from virtual_library.ui import BookDownloaderApp
            BookDownloaderApp().run()


if __name__ == '__main__':
    RegisterWindow().run()
