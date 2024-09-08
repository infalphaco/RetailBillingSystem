import sqlite3
import os
import sys
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import hashlib
from Connection.Connection import Connection

class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.root.resizable(False, False)
        self.root.title("FIREFIX RETAIL BILLING SYSTEM ADMINPANEL|Login")
        self.root['bg'] = '#7575a3'
        icon_path = self.resource_path("img/icon.ico")
        self.root.iconbitmap(icon_path)

        # Get the screen width and height
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Calculate the x and y coordinates to center the window
        x = (screen_width - 500) // 2
        y = (screen_height - 350) // 2

        # Set the window position
        self.root.geometry(f'500x350+{x}+{y}')

        self.conn = sqlite3.connect('db/retail_billing.db')
        self.cursor = self.conn.cursor()

        self.create_widgets()

    def resource_path(self, relative_path):
        """ Get absolute path to resource, works for dev and for PyInstaller """
        if getattr(sys, 'frozen', False):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)

    def create_widgets(self):
        # Title
        self.tittle = tk.Label(self.root, text="Admin Panel", font=(
            'Georgia', 20, 'bold'), bg='#7575a3')
        self.tittle.place(x=160, y=15)

        self.label_frame = tk.LabelFrame(
            root, text="Log In", bg="#7575a3", font=('Georgia', 10, 'bold'))
        self.label_frame.place(x=20, y=60)

        self.username_label = tk.Label(
            self.label_frame, text="Username:", bg='#7575a3', font=('Georgia', 12, 'bold'))
        self.username_label.grid(row=0, column=0, padx=5, pady=[30, 10])

        self.username_var = tk.StringVar()
        self.username_entry = tk.Entry(
            self.label_frame, textvariable=self.username_var, width=20, font=('Georgia', 15, 'bold'))
        self.username_entry.grid(row=0, column=1, padx=20, pady=[30, 10])

        self.password_label = tk.Label(
            self.label_frame, text="Password:", font=('Georgia', 12, 'bold'), bg='#7575a3')
        self.password_label.grid(row=3, column=0, padx=20, pady=[30, 10])

        self.password_var = tk.StringVar()
        self.password_entry = ttk.Entry(
            self.label_frame, textvariable=self.password_var, width=20, font=('Georgia', 15, 'bold'), show='*')
        self.password_entry.grid(row=3, column=1, padx=20, pady=[30, 10])

        self.login_button = tk.Button(self.label_frame, text="Login", command=self.login,
                                      width=22, height=2, font=('Georgia', 10, 'bold'), bg="blue")
        self.login_button.grid(row=4, column=1,  padx=10, pady=[30, 40])

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def login(self):
        username = self.username_var.get()
        password = self.password_var.get()

        if not username or not password:
            messagebox.showerror(
                "Login Error", "Please enter both username and password.")
            return

        hashed_password = self.hash_password(password)
        # print(hashed_password)
        
        # Check if the user exists in the database
        self.cursor.execute(
            "SELECT * FROM users WHERE username=? AND password=? AND category='Admin'", (username, hashed_password))
        user = self.cursor.fetchone()

        if user:
            # If the user exists, close the login window and open the main billing application
            self.root.destroy()
            root = tk.Tk()
            app = Users(root)
            root.mainloop()
        else:
            messagebox.showerror(
                "Login Failed", "Invalid username or password or you are not admin!")

class Users:

    def __init__(self, root):
        self.categories = ['Select', 'Admin', 'Cashier']
        # Create the main application window
        root.title('FIREFIX RETAIL BILLING SYSTEM|Users')
        root.resizable(False, False)
        root['bg'] = '#a7a5cc'
        icon_path = self.resource_path("img/icon.ico")
        root.iconbitmap(icon_path)

        # Get the screen width and height
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()

        # Calculate the x and y coordinates to center the window
        x = (screen_width - 1200) // 2
        y = (screen_height - 600) // 2

        # Set the window position
        root.geometry(f'1200x600+{x}+{y}')

        # Tittle
        self.title_frame = tk.LabelFrame(root, bg="#7575a3")
        self.title_frame.place(x=20, y=18)

        self.title = tk.Label(self.title_frame, text="Users", font=(
            'Georgia', 20, 'bold'), bg='#7575a3')
        self.title.grid(row=0, column=2, pady=[5, 5], padx=[530, 530])

        # Create and place input fields and buttons
        self.label_fullname = tk.Label(root, text='Full Name           ', font=(
            'Georgia', 12, 'bold'), bg='#a7a5cc')
        self.label_fullname.place(x=120, y=410)
        self.entry_fullname = tk.Entry(root, font=(
            'Georgia', 12, 'bold'), width=25)
        self.entry_fullname.place(x=400, y=410)

        self.label_username = tk.Label(root, text='Username            ', font=(
            'Georgia', 12, 'bold'), bg='#a7a5cc')
        self.label_username.place(x=120, y=450)
        self.entry_username = tk.Entry(root, font=(
            'Georgia', 12, 'bold'), width=25)
        self.entry_username.place(x=400, y=450)

        self.label_password = tk.Label(root, text='Password             ', font=(
            'Georgia', 12, 'bold'), bg='#a7a5cc')
        self.label_password.place(x=120, y=490)
        self.entry_password = tk.Entry(root, show='*', font=(
            'Georgia', 12, 'bold'), width=25)
        self.entry_password.place(x=400, y=490)

        # Create and place the category dropdown
        label_category = tk.Label(root, text='Category               ', font=(
            'Georgia', 12, 'bold'), bg='#a7a5cc')
        label_category.place(x=120, y=530)
        self.selected_category = tk.StringVar(root)
        dropdown_category = tk.OptionMenu(
            root, self.selected_category, *self.categories)
        # Set the default selected category
        self.selected_category.set(self.categories[0])
        dropdown_category.config(font=('Georgia', 8), width=26, height=1)
        dropdown_category.place(x=400, y=530)

        self.btn_add_user = tk.Button(
            root, text='Add User', command=self.add_user, width=20, height=2, bg="#5037F0")
        self.btn_add_user.place(x=820, y=400)

        self.btn_dlt_users = tk.Button(
            root, text='Delete Users', command=self.dlt_users, width=20, height=2, bg="red")
        self.btn_dlt_users.place(x=820, y=460)

        self.btn_edit_users = tk.Button(
            root, text='Edit Users', command=self.edit_users, width=20, height=2, bg='#03dffc')
        self.btn_edit_users.place(x=820, y=520)

        # Create and place a treeview to display the users
        self.tree = ttk.Treeview(root, columns=(
            "c1", "c2", "c3", "c4", "c5", "c6"), show="headings", height=13)
        self.tree.column('#1', anchor='center', width=100)
        self.tree.heading('c1', text='ID')
        self.tree.column('#2', anchor='center', width=300)
        self.tree.heading('c2', text='Full Name')
        self.tree.column('#3', anchor='center', width=250)
        self.tree.heading('c3', text='Username')
        self.tree.column('#4', anchor='center', width=200)
        self.tree.heading('c4', text='Password')
        self.tree.column('#5', anchor='center', width=100)
        self.tree.heading('c5', text='Category')
        self.tree.column('#6', anchor='center', width=200)
        self.tree.heading('c6', text='Timestamp')
        self.tree.place(x=20, y=90)

        # Call the show_users function to populate the treeview initially
        self.show_users()

    # Create a connection to the SQLite database
    conn = sqlite3.connect('db/retail_billing.db')
    cursor = conn.cursor()

    def resource_path(self, relative_path):
        """ Get absolute path to resource, works for dev and for PyInstaller """
        if getattr(sys, 'frozen', False):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    # Function to insert a new user into the database
    def add_user(self):
        fullname = self.entry_fullname.get()
        username = self.entry_username.get()
        password = self.entry_password.get()
        category = self.selected_category.get()

        if fullname and username and password and category:
            hashed_password = self.hash_password(password)
            # Insert the user data into the database
            self.cursor.execute("INSERT INTO users (fullname, username, password, category) VALUES (?, ?, ?, ?)",
                                (fullname, username, hashed_password, category))

            # Commit the changes
            self.conn.commit()

            # Clear the input fields after adding a user
            self.entry_fullname.delete(0, tk.END)
            self.entry_username.delete(0, tk.END)
            self.entry_password.delete(0, tk.END)

        else:
            messagebox.showerror("Error", "Please enter all details!")

        self.show_users()

    # Function to display the current users in the database
    def show_users(self):
        self.cursor.execute("SELECT * FROM users")
        users = self.cursor.fetchall()

        # Clear the existing contents in the treeview
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Insert the users from the database into the treeview
        for user in users:
            self.tree.insert('', tk.END, values=user)

    def dlt_users(self):
        select_user = self.tree.selection()
        if messagebox.askyesno("Delete User", "Are you sure delete this user?"):         
            if select_user:
                for user in select_user:
                    # Retrieve the record ID
                    record_id = self.tree.item(user)['values'][0]
                    self.tree.delete(user)
                    self.cursor.execute(
                        '''DELETE FROM users WHERE id = ?''', (record_id,))
                    self.conn.commit()

    def edit_users(self):
        select_user = self.tree.selection()
        if not select_user:
            messagebox.showerror("Error", "Please select a product to edit.")
            return

        user_values = self.tree.item(select_user[0], "values")
        id = user_values[0]
        old_fullname = user_values[1]
        old_username = user_values[2]
        old_password = user_values[3]
        old_category = user_values[4]

        new_fullname = simpledialog.askstring(
            "Edit User", "Enter new full name:", initialvalue=old_fullname)
        if new_fullname is None:
            return

        new_username = simpledialog.askstring(
            "Edit User", "Enter new username:", initialvalue=old_username)
        if new_username is None:
            return

        new_password = simpledialog.askstring(
            "Edit User", "Enter new password:", initialvalue=old_password, show="*")
        if new_password is None:
            return

        new_category = simpledialog.askstring(
            "Edit User", "Enter new category:", initialvalue=old_category)
        if new_category is None:
            return

        hashed_password = self.hash_password(new_password)
        
        self.cursor.execute("UPDATE users SET fullname= ?, username = ?, password = ?, category = ? WHERE id = ?",
                            (new_fullname, new_username, hashed_password, new_category, id))

        self.conn.commit()
        self.show_users()
        messagebox.showinfo("Success", "User edited successfully.")

if __name__ == "__main__":
    root = tk.Tk()
    conn = Connection('db/retail_billing.db')
    conn.create_database_tables()
    login_window = LoginWindow(root)
    root.mainloop()