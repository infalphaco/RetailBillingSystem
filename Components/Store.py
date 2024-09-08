import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
import sqlite3
import tkinter as sys
import os

class Store:
    def __init__(self, root):
        self.root = root
        self.root.title("FIREFIX RETAIL BILLING SYSTEM|Store Panel")
        self.root.resizable(False, False)
        self.root['bg'] = '#a7a5cc'

        # Get the screen width and height
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Calculate the x and y coordinates to center the window
        x = (screen_width - 800) // 2
        y = (screen_height - 450) // 2

        # Set the window position
        self.root.geometry(f'800x450+{x}+{y}')

        # Create and connect to the database
        self.conn = sqlite3.connect("db/retail_billing.db")
        self.cursor = self.conn.cursor()

        # Tittle
        self.title_frame = tk.LabelFrame(self.root, bg="#7575a3")
        self.title_frame.place(x=20, y=10)

        self.title = tk.Label(self.title_frame, text="STORE", font=(
            'Georgia', 20, 'bold'), bg='#7575a3')
        self.title.grid(row=0, column=2, pady=[5, 5], padx=[326, 326])

        # Create GUI elements
        self.product_tree = ttk.Treeview(root, columns=(
            "c1", "c2", "c3", "c4"), show="headings", height=17)
        self.product_tree.column("#1", anchor="center", width=200)
        self.product_tree.heading("c1", text="Product Name")
        self.product_tree.column("#2", anchor="center", width=100)
        self.product_tree.heading("c2", text="Unit Price")
        self.product_tree.column("#3", anchor="center", width=100)
        self.product_tree.heading("c3", text="Stock")
        self.product_tree.column("#4", anchor="center", width=200)
        self.product_tree.heading("c4", text="Date Time")
        self.product_tree.place(x=20, y=70)

        # Create a custom style with increased row margin
        custom_style = ttk.Style()
        # Change the padding between rows as per your requirement
        custom_style.configure("Custom.Treeview", rowmargins=10)

        # Apply the custom style to the Treeview widget
        self.product_tree.configure(style="Custom.Treeview")

        self.add_button = tk.Button(root, text="Add Product", command=self.add_product, height=2, width=18, font=(
            'Georgia', 8, 'bold'), bg='#5037F0')
        self.add_button.place(x=630, y=70)

        self.edit_button = tk.Button(root, text="Edit Product", command=self.edit_product, height=2, width=18, font=(
            'Georgia', 8, 'bold'), bg="#03dffc")
        self.edit_button.place(x=630, y=130)

        self.delete_button = tk.Button(root, text="Delete Product", command=self.delete_product, height=2, width=18, font=(
            'Georgia', 8, 'bold'), bg="red")

        self.delete_button.place(x=630, y=190)
        # Populate product tree
        self.populate_product_tree()

    def resource_path(self, relative_path):
        """ Get absolute path to resource, works for dev and for PyInstaller """
        if getattr(sys, 'frozen', False):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)

    def add_product(self):
        new_name = simpledialog.askstring("Add Product", "Enter product name:")
        if new_name is None:
            return

        new_price = simpledialog.askfloat(
            "Add Product", "Enter product price:")
        if new_price is None:
            return

        self.cursor.execute(
            "INSERT INTO CSV_data (item_name, unit_price) VALUES (?, ?)", (new_name, new_price))
        self.conn.commit()
        self.populate_product_tree()
        messagebox.showinfo("Success", "Product added successfully.")

    def edit_product(self):
        selected_item = self.product_tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a product to edit.")
            return

        item_values = self.product_tree.item(selected_item[0], "values")
        old_name = item_values[0]
        old_price = item_values[1]
        old_stock = item_values[2]

        new_name = simpledialog.askstring(
            "Edit Product", "Enter new name:", initialvalue=old_name)
        if new_name is None:
            return

        new_price = simpledialog.askfloat(
            "Edit Product", "Enter new price:", initialvalue=old_price)
        if new_price is None:
            return
        
        new_stock = simpledialog.askfloat(
            "Edit Product", "Enter new stock:", initialvalue=old_stock)
        if new_stock is None:
            return

        self.cursor.execute(
            "UPDATE csv_data SET item_name = ?, unit_price = ?, stock = ? WHERE item_name = ?", (new_name, new_price, new_stock, old_name))
        self.conn.commit()
        self.populate_product_tree()
        messagebox.showinfo("Success", "Product edited successfully.")

    def populate_product_tree(self):
        self.product_tree.delete(*self.product_tree.get_children())
        self.cursor.execute("SELECT item_name, unit_price, stock, timestamp FROM CSV_data")
        products = self.cursor.fetchall()
        for product in products:
            self.product_tree.insert("", "end", values=product)

    def delete_product(self):
        selected_item = self.product_tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a product to delete.")
            return

        item_values = self.product_tree.item(selected_item[0], "values")
        product_name = item_values[0]

        confirm = messagebox.askyesno(
            "Confirm Deletion", f"Are you sure you want to delete '{product_name}'?")
        if confirm:
            self.cursor.execute(
                "DELETE FROM CSV_data WHERE item_name = ?", (product_name,))
            self.conn.commit()
            self.populate_product_tree()
            messagebox.showinfo(
                "Success", f"Product '{product_name}' deleted successfully.")