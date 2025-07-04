import tkinter as tk
from tkinter import ttk
import sqlite3
from tkinter import messagebox

username1='example@email.com'
password1='$your-password%'


# Connect to the Sqlite data base
conn = sqlite3.connect('password_manager.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS passwords (
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    website TEXT NOT NULL,
    usernameTEXT NOT NULL,
    password TEXT NOT NULL)''')
conn.commit()

# app set up
root = tk.Tk()
root.title('Password Manager')

# size of the app
root.geometry("400x600")
root.resizable(False,False)

# home page

# text labels
instructions = tk.Label(root, text='     welcome to your password manager,',  font="Arial", justify="center")
intrusion = tk.Label(root, text="")
instructions1 = tk.Label(root, text='   to continue, please login.', font='Arial', justify='center')

# Authentication label

Username = tk.Label(root, text="username")
password = tk.Label(root, text="password")

# login Authentication


login = tk.Entry(root, width=65)
login1 = tk.Entry(root, width=65, show="*")

# login function
def handle_login():
    username = login.get()
    password = login1.get()
    
    # validation statements
    if Username and password:
        print(f"login attempt - Username: {username}")
        # logic for authentication
        if username == username1 and password == password1:
            print("login successful")
            
    else:
        print("please enter both the Username and Password sections")


# login button

login_btn = tk.Button(root, text="login", command=handle_login, width=15)

# display the home page

instructions.grid(row=1, column=0)
intrusion.grid(row=2)
instructions1.grid(row=3, column=0)

# login process
intrusion.grid(row=4)
Username.grid(row=5, column=0, sticky='W')
login.grid(row=6, column=0, sticky='w')
password.grid(row=7, column=0, sticky='w')
login1.grid(row=8, column=0, sticky='w')
login_btn.grid(row=9, column=0)



# #functions to add and delete functions
# def add_password():
#     website = website_entry.get()
#     username = username_entry.get()
#     password = password_entry.get()
    
#     if website and username and password:
#         cur.execute("INSERT INTO passwords (website, username, password) VALUES (?,?,?)",
#                     (website, username, password))
#         conn.commit()
#         messagebox.showinfo("Success", "Password added successfully")
#     else:
#         messagebox.showwarning("Warning", "Please fill all fields")

# Configure column weight for proper resizing
root.grid_columnconfigure(0, weight=1)


root.mainloop()

