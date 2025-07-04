import tkinter as tk
from tkinter import messagebox, filedialog
import sqlite3
import csv

# Credentials
username1 = 'example@email.com'
password1 = '$your-password%'

# Database setup
conn = sqlite3.connect('password_manager.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS passwords (
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    website TEXT NOT NULL,
    usernameTEXT TEXT NOT NULL,
    password TEXT NOT NULL)''')
conn.commit()

# Main App Class
class PasswordManagerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Password Manager")
        self.geometry("400x650")
        self.resizable(False, False)
        self.user_name = ""

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
        if page == HomePage:
            frame.update_welcome(self.user_name)
        frame.tkraise()

# Login Page
class LoginPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        tk.Label(self, text="Welcome to your password manager", font=("Arial", 14)).pack(pady=10)
        tk.Label(self, text="Please login", font=("Arial", 12)).pack(pady=5)

        tk.Label(self, text="Username").pack()
        self.username_entry = tk.Entry(self, width=30, justify='center')
        self.username_entry.pack()

        tk.Label(self, text="Password").pack()
        self.password_entry = tk.Entry(self, show="*", width=30, justify='center')
        self.password_entry.pack()

        tk.Label(self, text="Name").pack()
        self.name_entry = tk.Entry(self, width=30, justify='center')
        self.name_entry.pack()

        tk.Button(self, text="Login", command=self.login).pack(pady=10)

    def login(self):
        if (self.username_entry.get() == username1 and 
            self.password_entry.get() == password1):
            self.controller.user_name = self.name_entry.get()
            self.controller.show_frame(HomePage)
        else:
            messagebox.showerror("Error", "Invalid credentials")

# Home Page
class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Top bar
        top_frame = tk.Frame(self)
        top_frame.pack(fill='x', pady=10)
        tk.Button(top_frame, text="Logout", command=lambda: controller.show_frame(LoginPage)).pack(side='right', padx=10)

        self.welcome_label = tk.Label(self, text="", font=("Arial", 14))
        self.welcome_label.pack(pady=10)

        # Search bar
        tk.Label(self, text="Search by Website").pack()
        self.search_entry = tk.Entry(self, width=30, justify='center')
        self.search_entry.pack()
        self.search_entry.bind("<KeyRelease>", lambda event: self.refresh_passwords())

        # Entry fields
        for label in ["Website", "Username", "Password"]:
            tk.Label(self, text=label).pack()
            setattr(self, f"{label.lower()}_entry", tk.Entry(self, width=30, justify='center'))
            getattr(self, f"{label.lower()}_entry").pack()

        # Buttons
        tk.Button(self, text="Add Password", command=self.add_password).pack(pady=5)
        tk.Button(self, text="Delete Selected", command=self.delete_password).pack(pady=5)
        tk.Button(self, text="Export to CSV", command=self.export_passwords).pack(pady=5)

        # Listbox
        self.password_list = tk.Listbox(self, width=50)
        self.password_list.pack(pady=10)

        self.refresh_passwords()

    def update_welcome(self, name):
        self.welcome_label.config(text=f"Welcome, {name}!")
        self.refresh_passwords()

    def add_password(self):
        website = self.website_entry.get()
        username = self.username_entry.get()
        password = self.password_entry.get()

        if website and username and password:
            c.execute("INSERT INTO passwords (website, usernameTEXT, password) VALUES (?, ?, ?)",
                      (website, username, password))
            conn.commit()
            messagebox.showinfo("Success", "Password added!")
            self.refresh_passwords()
        else:
            messagebox.showwarning("Warning", "Please fill all fields")

    def delete_password(self):
        selected = self.password_list.curselection()
        if selected:
            item = self.password_list.get(selected[0])
            record_id = item.split(" | ")[0]
            c.execute("DELETE FROM passwords WHERE id=?", (record_id,))
            conn.commit()
            messagebox.showinfo("Deleted", "Password deleted.")
            self.refresh_passwords()
        else:
            messagebox.showwarning("Warning", "Select an item to delete")

    def export_passwords(self):
        c.execute("SELECT website, usernameTEXT, password FROM passwords ORDER BY website ASC")
        rows = c.fetchall()
        file_path = filedialog.asksaveasfilename(defaultextension=".csv",
                                                 filetypes=[("CSV files", "*.csv")])
        if file_path:
            with open(file_path, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['Website', 'Username', 'Password'])
                writer.writerows(rows)
            messagebox.showinfo("Exported", f"Passwords exported to {file_path}")

    def refresh_passwords(self):
        self.password_list.delete(0, tk.END)
        search_term = self.search_entry.get().lower()
        c.execute("SELECT id, website, usernameTEXT FROM passwords")
        rows = c.fetchall()
        rows.sort(key=lambda x: x[1].lower())  # Sort by website
        for row in rows:
            if search_term in row[1].lower():
                self.password_list.insert(tk.END, f"{row[0]} | {row[1]} | {row[2]}")

# Run the app
if __name__ == "__main__":
    app = PasswordManagerApp()
    app.mainloop()



