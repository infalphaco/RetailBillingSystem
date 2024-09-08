import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import sqlite3
import os

class BillViewerApp:
    def __init__(self, root):
        self.root = root
        self.conn = sqlite3.connect('db/retail_billing.db')
        self.root['bg'] = "#a7a5cc"
        self.cursor = self.conn.cursor()
        self.root.title("Bill Viewer")
        
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - 900) // 2
        y = (screen_height - 500) // 2
        self.root.geometry(f'900x500+{x}+{y}')

        self.search_var = tk.StringVar()
        self.search_entry = tk.Entry(root, textvariable=self.search_var, width=30)
        self.search_entry.pack(pady=(10, 10))
        
        self.search_button = tk.Button(root, text="SEARCH", command=self.search_bills, font=(
            'Georgia', 12, 'bold'), bg='blue')
        self.search_button.pack(pady=(10, 10))

        self.tree = ttk.Treeview(root, columns=("c1","c2", "c3"), show="headings", height=12)
        self.tree.column("#1", anchor="center")
        self.tree.column("#2", anchor="center")
        self.tree.column("#3", anchor="center")     
        self.tree.heading("c1", text="Bill Number")
        self.tree.heading("c2", text="Date and Time")  
        self.tree.heading("c3", text="Total Amount")  
        self.tree.pack()

        self.load_data()

        self.delete_button = tk.Button(root, text="Delete Selected", command=self.delete_selected, font=(
            'Georgia', 12, 'bold'), bg='red')
        self.delete_button.pack(pady=(30, 0))

        # self.print_button = tk.Button(root, text="Print Selected", command=self.print_selected, font=(
        #     'Georgia', 12, 'bold'), bg='green')
        # self.print_button.pack(pady=(10, 10))

    def load_data(self):
        self.cursor.execute("SELECT bill_number, timestamp, total_amount FROM bills")
        bills = self.cursor.fetchall()
        for bill in bills:
            self.tree.insert("", "end", values=bill)

    def search_bills(self):
        search_term = self.search_var.get()
        self.tree.delete(*self.tree.get_children())  # Clear the Treeview
        self.cursor.execute("SELECT bill_number, timestamp, total_amount FROM bills WHERE bill_number LIKE ?", ('%' + search_term + '%',))
        bills = self.cursor.fetchall()
        for bill in bills:
            self.tree.insert("", "end", values=bill)

    def delete_selected(self):
        if messagebox.askyesno("Delete Bill", "Do you want to delete this bill?"):
            selected_indices = self.tree.selection()
            if selected_indices:
                selected_index = selected_indices[0]
                item_values = self.tree.item(selected_index, "values")
                bill_number = item_values[0]

                # Perform deletion from the database
                self.cursor.execute("DELETE FROM bills WHERE bill_number = ?", (bill_number,))
                self.conn.commit()

                # Remove the selected item from the tree view
                self.tree.delete(selected_index)

            else:
                messagebox.showwarning("No Selection", "Please select a bill to delete.")