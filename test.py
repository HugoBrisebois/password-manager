import tkinter as tk
from tkinter import messagebox
import sqlite3

username1 = 'example@email.com'
password1 = '$your-password%'

# Database setup
conn = sqlite3.connect('password_manager.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS passwords (
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    website TEXT NOT NULL,
    usernameTEXT NOT NULL,
    password TEXT NOT NULL)''')
conn.commit()

# Main App Class
class PasswordManagerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Password Manager")
        self.geometry("400x600")
        self.resizable(False, False)

        container = tk.Frame(self)
        container.pack(fill="both", expand=True)

        self.frames = {}
        for F in (LoginPage, HomePage):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(LoginPage)

    def show_frame(self, page):
        frame = self.frames[page]
        frame.tkraise()

# Login Page
class LoginPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        tk.Label(self, text="Welcome to your password manager").pack(pady=10)
        tk.Label(self, text="Please login").pack()

        tk.Label(self, text="Username").pack()
        self.username_entry = tk.Entry(self)
        self.username_entry.pack()

        tk.Label(self, text="Password").pack()
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.pack()

        tk.Button(self, text="Login", command=lambda: self.login(controller)).pack(pady=10)

    def login(self, controller):
        if (self.username_entry.get() == username1 and 
            self.password_entry.get() == password1):
            controller.show_frame(HomePage)
        else:
            messagebox.showerror("Error", "Invalid credentials")

# Home Page
class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        tk.Label(self, text="Welcome to the Home Page!").pack(pady=20)
        tk.Button(self, text="Logout", command=lambda: controller.show_frame(LoginPage)).pack()

# Run the app
if __name__ == "__main__":
    app = PasswordManagerApp()
    app.mainloop()
