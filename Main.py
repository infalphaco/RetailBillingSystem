import tkinter as tk
from Components.LoginWindow import LoginWindow
from Connection.Connection import Connection
import os

if __name__ == "__main__":
    # Ensure the database directory exists
    db_file = 'db/retail_billing.db'
    db_dir = os.path.dirname(db_file)
    if db_dir and not os.path.exists(db_dir):
        os.makedirs(db_dir)
    
    # Create the database connection and initialize tables
    conn = Connection(db_file)
    
    # Create the login window
    root = tk.Tk()
    login_window = LoginWindow(root)
    root.mainloop()
