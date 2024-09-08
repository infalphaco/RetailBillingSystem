import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import os
import sys
from sqlite3 import Error
import hashlib
from Components.RetailBillingApp import RetailBillingApp

class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.root.resizable(False, False)
        self.root.title("FIREFIX RETAIL BILLING SYSTEM | Login")
        self.root['bg'] = '#a7a5cc'
        icon_path = self.resource_path("img/icon.ico")

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - 500) // 2
        y = (screen_height - 350) // 2
        self.root.geometry(f'500x350+{x}+{y}')

        self.conn = sqlite3.connect('db/retail_billing.db')
        self.cursor = self.conn.cursor()

        self.create_widgets()

    def resource_path(self, relative_path):
        if getattr(sys, 'frozen', False):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)
    
    def log_user_login(self, user_id, full_name):
        try:
            self.cursor.execute("INSERT INTO login_history (user_id, full_name) VALUES (?, ?)", (user_id, full_name))
            self.conn.commit()
        except Error as e:
            print(f"Error logging user login: {e}")

    # Example usage in login logic
    def user_login(self, username, password):
        self.cursor.execute("SELECT id, fullname FROM users WHERE username = ? AND password = ?", (username, password))
        user = self.cursor.fetchone()
        if user:
            user_id = user[0]
            full_name = user[1]
            self.log_user_login(user_id, full_name)
            print("Login successful")
        else:
            print("Invalid credentials")

    def create_widgets(self):
        self.title = tk.Label(self.root, text="RETAIL BILLING SYSTEM", font=('Georgia', 18, 'bold'), bg='#a7a5cc')
        self.title.place(x=100, y=15)

        self.label_frame = tk.LabelFrame(self.root, text="Log In", bg="#a7a5cc", font=('Georgia', 10, 'bold'))
        self.label_frame.place(x=20, y=60)

        self.username_label = tk.Label(self.label_frame, text="Username:", bg='#a7a5cc', font=('Georgia', 12, 'bold'))
        self.username_label.grid(row=0, column=0, padx=5, pady=[30, 10])

        self.username_var = tk.StringVar()
        self.username_entry = tk.Entry(self.label_frame, textvariable=self.username_var, width=20, font=('Georgia', 15, 'bold'))
        self.username_entry.grid(row=0, column=1, padx=20, pady=[30, 10])

        self.password_label = tk.Label(self.label_frame, text="Password:", font=('Georgia', 12, 'bold'), bg='#a7a5cc')
        self.password_label.grid(row=3, column=0, padx=20, pady=[30, 10])

        self.password_var = tk.StringVar()
        self.password_entry = ttk.Entry(self.label_frame, textvariable=self.password_var, width=20, font=('Georgia', 15, 'bold'), show='*')
        self.password_entry.grid(row=3, column=1, padx=20, pady=[30, 10])

        self.login_button = tk.Button(self.label_frame, text="Login", command=self.login, width=22, height=2, font=('Georgia', 10, 'bold'), bg="blue")
        self.login_button.grid(row=4, column=1, padx=10, pady=[30, 40])

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def login(self):
        username = self.username_var.get()
        password = self.password_var.get()

        if not username or not password:
            messagebox.showerror("Login Error", "Please enter both username and password.")
            return

        hashed_password = self.hash_password(password)
        self.cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, hashed_password))
        user = self.cursor.fetchone()

        if user:
            self.logged_in_user = user[1]  # Assuming the username is the second column
            self.root.destroy()
            self.user_login(username, hashed_password)
            root = tk.Tk()
            app = RetailBillingApp(root, self.logged_in_user)
            root.mainloop()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")
