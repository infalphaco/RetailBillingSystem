import tkinter as tk
import tkinter as sys
from tkinter import ttk, simpledialog, messagebox, filedialog
import sqlite3
from sqlite3 import Error
import os
import subprocess
from Components.Calculator import Calculator
from Components.DataStoreApp import DataStoreApp
from Components.BillViewerApp import BillViewerApp
from Components.Store import Store
from Components.Reports import Reports
import time
import pandas as pd

class RetailBillingApp:
    def __init__(self, root, logged_in_user):
        self.root = root
        self.root.title("FIREFIX RETAIL BILLING SYSTEM")
        self.root.resizable(False, False)
        self.root['bg'] = '#a7a5cc'
        self.logged_in_user = logged_in_user  # Make sure this line exists

        # Get the screen width and height
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Calculate the x and y coordinates to center the window
        x = (screen_width - 1400) // 2
        y = (screen_height - 700) // 3

        # Set the window position
        self.root.geometry(f'1400x700+{x}+{y}')

        self.conn = sqlite3.connect("db/retail_billing.db")
        self.cursor = self.conn.cursor()

        self.create_widgets()

    def resource_path(self, relative_path):
        """ Get absolute path to resource, works for dev and for PyInstaller """
        if getattr(sys, 'frozen', False):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)
        

    def resource_path(self, relative_path):
        """ Get absolute path to resource, works for dev and for PyInstaller """
        if getattr(sys, 'frozen', False):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)

    def add_product_window(self):
        # Open the Store window
        store_window = tk.Toplevel(self.root)
        store_app = Store(store_window)
        
    def show_bills(self):
        # Open the Store window
        bills_window = tk.Toplevel(self.root)
        bills_app = BillViewerApp(bills_window)
        
    def data_store(self):
        data_window = tk.Toplevel(self.root)
        bill_app = DataStoreApp(data_window)

    def calculator(self):
        cal_window = tk.Toplevel(self.root)
        cal_app = Calculator(cal_window)

    def reports(self):
        report_window = tk.Toplevel(self.root)
        report_app = Reports(report_window)

    def update_product_combobox(self):
        self.products = self.fetch_products()
        self.product_combobox["values"] = self.products

    def on_entry_click(self, event):
        if self.search_entry.get() == 'Search Here':
            self.search_entry.delete(0, tk.END)
            # Use a lighter shade of grey (adjust the value as needed)
            self.search_entry.config(fg='gray60')

    def on_focus_out(self, event):
        if self.search_entry.get() == '':
            self.search_entry.insert(0, 'Search Here')
            # Restore the original text color (black or your desired color)
            self.search_entry.config(fg='black')

    
    def filter_products(self, event):
        search_term = self.search_var.get()
        products = self.fetch_products()  # Fetch the list of all products
        filtered_products = [
            product for product in products if search_term.lower() in product.lower()]
        self.product_combobox["values"] = filtered_products

        if not filtered_products:
            # Clear the selection if the filtered list is empty
            self.product_var.set("")
        elif search_term.lower() != filtered_products[0].lower():
            # Auto-select the first item if it matches the search
            self.product_var.set(filtered_products[0])

    def delete_selected_item(self):
        selected_indices = self.items_table.selection()
        if selected_indices:
            selected_index = selected_indices[0]
            item_values = self.items_table.item(selected_index, "values")
            product_name, quantity_str = item_values[0], item_values[1]
            selected_item = f"{product_name} x{quantity_str}"

            # Find the corresponding index in the cart_list
            index_to_remove = None
            for idx, item in enumerate(self.cart_list):
                if item[0] == product_name:  # Check only product name
                    index_to_remove = idx
                    break

            if index_to_remove is not None:
                # Retrieve the quantity to update the total amount
                quantity = int(quantity_str)

                # Retrieve product id from the database
                self.cursor.execute(
                    "SELECT id FROM csv_data WHERE item_name=?", (product_name,))
                product = self.cursor.fetchone()

                if product:
                    product_id = product[0]
                    # Update stock in the csv_data table
                    self.cursor.execute("UPDATE csv_data SET stock = stock + ? WHERE id = ?", (quantity, product_id))
                    self.conn.commit()

                # Remove the item from the cart_list
                self.cart_list.pop(index_to_remove)

                # Update the items_table after deleting the item
                self.items_table.delete(selected_index)

                # Update the total amount
                self.update_total_amount()

        else:
            # Product not found in the cart_list
            tk.messagebox.showerror(
                "Item Not Found", "The selected item does not exist in the cart.")
            

    def fetch_transactions(self):
        self.cursor.execute('SELECT * FROM bills')
        rows = self.cursor.fetchall()
        return rows


    def generate_and_print_bill(self):
        total_amount = self.total_var.get()

        if total_amount > 0:
            # Generating a bill number using timestamp
            bill_number = str(int(time.time()))  # Using current timestamp as bill number

            self.cursor.execute(
                "INSERT INTO bills (bill_number, total_amount) VALUES (?, ?)", (bill_number, total_amount))
            bill_id = self.cursor.lastrowid

            for item in self.cart_list:
                product_name, quantity = item
                self.cursor.execute(
                    "SELECT id FROM CSV_data WHERE item_name=?", (product_name,))
                product_id = self.cursor.fetchone()[0]

                self.cursor.execute(
                    "INSERT INTO bill_items (bill_id, product_id, quantity) VALUES (?, ?, ?)",
                    (bill_id, product_id, quantity)
                )

            self.conn.commit()
            self.reset_cart()  # Reset the cart and total amount after generating the bill

            # Ask the user if they want to print the bill
            if messagebox.askyesno("Print Bill", "Do you want to print the generated bill?"):
                self.print_bill(bill_number)
        else:
            messagebox.showinfo("Generate and Print Bill",
                                "No bill to generate and print.")
             

    def print_bill(self, bill_number):
        # Check if the bill exists in the database
        self.cursor.execute(
            "SELECT * FROM bills WHERE bill_number=?", (bill_number,))
        bill = self.cursor.fetchone()

        if bill:
            # Retrieve the bill details
            bill_id, _, _, _ = bill
            self.cursor.execute(
                "SELECT p.item_name, bi.quantity, p.unit_price FROM bill_items bi JOIN CSV_data p ON bi.product_id=p.id WHERE bi.bill_id=?", (bill_id,))
            items = self.cursor.fetchall()

            # Prepare the bill content
            bill_content = "\t\t\t\t\tGrocery Shop Name\n\n\n"
            bill_content += f"Bill Number: {bill_number}\n"
            bill_content += "------------------------------------------------------------\n"
            bill_content += "Item Name\t\tQuantity\t\tTotal Value\n"
            bill_content += "------------------------------------------------------------\n"

            total_amount = 0.0

            for item in items:
                name, quantity, price = item
                total_value = quantity * price
                bill_content += f"{name}\t\t\t{quantity}\t\t\t{total_value}\n"
                total_amount += total_value

            bill_content += "-------------------------------------------------------------\n"
            bill_content += f"Total Amount: {total_amount}\n"
            bill_content += "-------------------------------------------------------------\n"

            # Print the bill content using the default text editor
            with open("bill.txt", "w") as f:
                f.write(bill_content)

            os.startfile("bill.txt")

            subprocess.Popen(["notepad.exe", "/p", "bill.txt"], shell=True)

        else:
            messagebox.showerror(
                "Bill Not Found", "The specified bill number does not exist in the database.")

    def fetch_products(self):
        self.cursor.execute("SELECT item_name FROM CSV_data")
        products = self.cursor.fetchall()
        return [product[0] for product in products]

    def add_to_cart(self):
        product_name = self.product_var.get()
        quantity = self.quantity_var.get()

        if product_name and quantity > 0:
            # Check if the product is available in the product table
            self.cursor.execute(
                "SELECT id FROM csv_data WHERE item_name=?", (product_name,))
            product = self.cursor.fetchone()

            if product:
                product_id = product[0]
                # Call update_stock with correct parameters
                self.update_stock(product_id, quantity)

                # Check if the product is already in the cart
                existing_item_index = None
                for idx, item in enumerate(self.cart_list):
                    if item[0] == product_name:
                        existing_item_index = idx
                        break

                if existing_item_index is not None:
                    # If the product is already in the cart, update the quantity
                    self.cart_list[existing_item_index] = (
                        product_name, self.cart_list[existing_item_index][1] + quantity)
                else:
                    # If the product is not in the cart, add it
                    self.cart_list.append((product_name, quantity))

                # Update the items_table based on the current cart_list
                self.update_items_table()

                # Clear the product and quantity fields
                self.product_var.set("")
                self.quantity_var.set(0)

                # Update the total amount
                self.update_total_amount()
            else:
                tk.messagebox.showerror(
                    "Product Not Found", "The selected product does not exist in the product database.")
        else:
            tk.messagebox.showerror(
                "Invalid Input", "Please select a valid product and quantity.")
            
    def update_stock(self, product_id, sold_quantity):
        # transaction_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            # Retrieve current stock quantity
            self.cursor.execute("SELECT stock FROM csv_data WHERE id = ?", (product_id,))
            current_stock = self.cursor.fetchone()[0]
            
            # Update stock quantity after deducting sold items
            new_stock = current_stock - sold_quantity
            if new_stock < 0:
                tk.messagebox.showerror(
                    "Product not enough", "Not enough stock available for this product")
                
            else:
                # Update stock in the csv_data table
                self.cursor.execute("UPDATE csv_data SET stock = ? WHERE id = ?", (new_stock, product_id))
                self.conn.commit()
        except Error as e:
            print(e)
            
    def update_items_table(self):
        self.items_table.delete(*self.items_table.get_children())
        for item in self.cart_list:
            product_name, quantity = item
            self.items_table.insert("", "end", values=(product_name, quantity, self.get_product_price(
                product_name), self.get_total_value(product_name, quantity)))

        # Update the total amount
        self.update_total_amount()

    def update_total_amount(self):
        total_amount = 0.0
        for item in self.cart_list:
            product_name, quantity = item
            self.cursor.execute(
                "SELECT unit_price FROM CSV_data WHERE item_name=?", (product_name,))
            product = self.cursor.fetchone()

            if product:
                price = product[0]
                total_amount += price * quantity

                self.total_var.set(round(total_amount, 2))

    def update_total_value(self, index):
        # Update the total value for the item at the given index
        item_values = self.items_table.item(index, "values")
        quantity_str, price_str = item_values[1], item_values[2]
        quantity = int(quantity_str)
        price = float(price_str)
        total_value = quantity * price
        self.items_table.set(index, "c4", total_value)

    def export_data_to_excel(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")])
        if file_path:
            transactions = self.fetch_transactions()
            if transactions:
                df = pd.DataFrame(transactions, columns=["Transaction ID", "Bill Number", "Date and Time", "Total Amount"])
                df.to_excel(file_path, index=False)
                messagebox.showinfo("Export Data", f"Data exported successfully to {file_path}")
            else:
                messagebox.showinfo("Export Data", "No data available to export")

    def get_product_price(self, product_name):
        # Retrieve product price from the database
        self.cursor.execute(
            "SELECT unit_price FROM CSV_data WHERE item_name=?", (product_name,))
        product = self.cursor.fetchone()
        return product[0] if product else 0.0

    def get_total_value(self, product_name, quantity):
        # Calculate the total value for the given product and quantity
        price = self.get_product_price(product_name)
        return quantity * price
    
    def update_stock_quantity(self, item_name, new_stock_quantity, old_sold):
        try:
            self.cursor.execute(
                "SELECT stock FROM CSV_data WHERE item_name=?", (item_name,))
            currect_q = self.cursor.fetchone()  # Fetch the tuple
            current_stock = currect_q[0]  # Extract the integer value from the tuple
            # print(current_stock)
            new_stock = current_stock - (new_stock_quantity - old_sold)
            self.cursor.execute(
                "UPDATE csv_data SET stock = ? WHERE item_name = ?", (new_stock, item_name))
            self.conn.commit()
        except Error as e:
            print(e)

    def edit_item_quantity(self):
        selected_indices = self.items_table.selection()
        if selected_indices:
            selected_index = selected_indices[0]
            item_values = self.items_table.item(selected_index, "values")
            product_name, current_quantity_str = item_values[0], item_values[1]
            current_quantity = int(current_quantity_str)
            # print(current_quantity)

            new_quantity = simpledialog.askinteger(
                "Edit Quantity", f"Enter new quantity for {product_name}:", initialvalue=current_quantity)
            print(new_quantity)
            if new_quantity is not None:
                index_to_edit = None
                for idx, item in enumerate(self.cart_list):
                    if item[0] == product_name:
                        index_to_edit = idx
                        break

                if index_to_edit is not None:
                    diff_quantity = new_quantity - current_quantity
                    self.cart_list[index_to_edit] = (
                        product_name, new_quantity)
                    self.items_table.set(selected_index, "c2", new_quantity)
                    self.update_total_value(selected_index)
                    self.update_total_amount()

                    # Calculate old_sold (replace this with your actual calculation)
                    old_sold = current_quantity 

                    # Update stock quantity
                    self.update_stock_quantity(product_name, new_quantity, old_sold)
        else:
            tk.messagebox.showerror(
                "Item Not Found", "The selected item does not exist in the cart.")

    def generate_bill(self):
        total_amount = self.total_var.get()

        if total_amount > 0:
            bill_number = simpledialog.askstring(
                "Generate Bill", "Enter the bill number:")
            if bill_number:
                self.cursor.execute(
                    "INSERT INTO bills (bill_number, total_amount) VALUES (?, ?)", (bill_number, total_amount))
                bill_id = self.cursor.lastrowid

                for item in self.cart_list:
                    product_name, quantity = item
                    self.cursor.execute(
                        "SELECT id FROM products WHERE name=?", (product_name,))
                    product_id = self.cursor.fetchone()[0]

                    self.cursor.execute(
                        "INSERT INTO bill_items (bill_id, product_id, quantity) VALUES (?, ?, ?)",
                        (bill_id, product_id, quantity)
                    )

                self.conn.commit()
            self.reset_cart()  # Reset the cart and total amount after generating the bill

    def reset_cart(self):
        # Clear the cart list and the items table
        self.cart_list = []
        self.items_table.delete(*self.items_table.get_children())
        # Reset the total amount
        self.total_var.set(0.0)

    def show_profile(self):
        profile_window = tk.Toplevel(self.root)
        profile_window.title("Profile Information")
        profile_window.geometry("300x200")
        profile_window['bg'] = '#a7a5cc'

        # Displaying user profile information
        user_info = f"User: {self.logged_in_user}\n\nAdditional info here..."
        profile_label = tk.Label(profile_window, text=user_info, font=('Georgia', 12), bg='#a7a5cc')
        profile_label.pack(pady=20)

        # Close button
        close_button = tk.Button(profile_window, text="Close", command=profile_window.destroy, font=('Georgia', 12), bg='#42b6f5')
        close_button.pack(pady=10)
 
    def create_widgets(self):
        print("System Version: 1.10")

        # Create GUI components

        self.title_frame = tk.LabelFrame(self.root, bg="#7575a3")
        self.title_frame.place(x=30, y=20)

        self.title = tk.Label(self.title_frame, text="RETAIL BILLING SYSTEM", font=(
            'Georgia', 25, 'bold'), bg='#7575a3')
        self.title.grid(row=0, column=2, pady=[10, 10], padx=[435, 435])

        self.user_label = tk.Label(self.root, text=f"Logged in as: {self.logged_in_user}", font=('Georgia', 12, 'bold'), bg='#7575a3')
        self.user_label.grid(pady=[40, 10], padx=[1080, 435])

        self.label_frame = tk.LabelFrame(self.root, text="Create Order", bg="#7575a3", font=(
            'Georgia', 13, 'bold'))
        self.label_frame.place(x=30, y=100)

        self.search_var = tk.StringVar()
        self.search_entry = tk.Entry(
            self.label_frame, textvariable=self.search_var, width=38, font=('Georgia', 11, 'bold'))
        self.search_entry.grid(row=0, column=0, columnspan=2, padx=[
                               51, 30], pady=[20, 20])
        self.search_entry.insert(0, 'Search Here')
        self.search_entry.bind('<FocusIn>', self.on_entry_click)
        self.search_entry.bind('<FocusOut>', self.on_focus_out)
        self.search_entry.bind("<KeyRelease>", self.filter_products)

        self.product_label = tk.Label(self.label_frame, text="Product      :", font=(
            'Georgia', 13, 'bold'), bg='#7575a3')
        self.product_label.grid(row=1, column=0, pady=[15, 15])

        self.product_var = tk.StringVar()
        self.product_combobox = ttk.Combobox(self.label_frame, textvariable=self.product_var, width=15, font=(
            'Georgia', 13, 'bold'))
        self.product_combobox.grid(row=1, column=1, padx=[
                                   0, 30], pady=[15, 15])

        self.quantity_label = tk.Label(self.label_frame, text="Quantity    :", font=(
            'Georgia', 13, 'bold'), bg='#7575a3')
        self.quantity_label.grid(row=2, column=0, pady=[15, 15])

        self.quantity_var = tk.IntVar()
        self.quantity_entry = ttk.Entry(self.label_frame, textvariable=self.quantity_var, width=16, font=(
            'Georgia', 13, 'bold'))
        self.quantity_entry.grid(row=2, column=1, padx=[0, 30])

        self.add_button = tk.Button(self.label_frame, text="ADD ITEMS", command=self.add_to_cart, font=(
            'Georgia', 13, 'bold'), bg='#42b6f5', width=13, height=3)
        self.add_button.grid(row=3, column=0, pady=[15, 15], padx=[60, 0])

        self.delete_item_button = tk.Button(self.label_frame, text="DELETE ITEMS", command=self.delete_selected_item, font=(
            'Georgia', 13, 'bold'), bg='red', width=13, height=3)
        self.delete_item_button.grid(row=3, column=1, padx=[15, 15])

        self.edit_item_button = tk.Button(self.label_frame, text="EDIT QUANTITY", command=self.edit_item_quantity, font=(
            'Georgia', 13, 'bold'), bg='#f5c242', width=13, height=3)
        self.edit_item_button.grid(row=4, column=0, pady=[
                                    15, 15], padx=[60, 0])

        self.clear_cart_button = tk.Button(self.label_frame, text="CLEAR CART", command=self.reset_cart, font=(
            'Georgia', 13, 'bold'), bg='#900', width=13, height=3)
        self.clear_cart_button.grid(row=4, column=1, padx=[15, 15])

        self.total_label = tk.Label(self.label_frame, text="Total\n           Amount (Rs .)     :", font=(
            'Georgia', 13, 'bold'), bg='#7575a3')
        self.total_label.grid(row=5, column=0, pady=[15, 15], padx=[10, 0])

        self.total_var = tk.DoubleVar()
        self.total_entry = ttk.Entry(self.label_frame, textvariable=self.total_var, state="readonly", font=(
            'Georgia', 15, 'bold'), width=12)
        self.total_entry.grid(row=5, column=1, padx=[20, 20])

        self.print_bill_button = tk.Button(self.label_frame, text="GENERATE AND PRINT BILL", command=self.generate_and_print_bill,  font=(
            'Georgia', 13, 'bold'), bg='#60f542', width=30, height=2)
        self.print_bill_button.grid(row=6, column=0, columnspan=2, padx=[
                                    45, 20], pady=[20, 33])

        self.table_frame = tk.LabelFrame(self.root, bg="#7575a3", font=(
            'Georgia', 13, 'bold'))
        self.table_frame.place(x=520, y=100)

        self.items_table = ttk.Treeview(self.table_frame, columns=(
            "c1", "c2", "c3", "c4"), show="headings", height=26)
        self.items_table.column("#1", anchor="center", width=200)
        self.items_table.column("#2", anchor="center", width=80)
        self.items_table.column("#3", anchor="center", width=120)
        self.items_table.column("#4", anchor="center")
        self.items_table.heading("c1", text="Item")
        self.items_table.heading("c2", text="Quantity")
        self.items_table.heading("c3", text="Unit Price")
        self.items_table.heading("c4", text="Total Value")
        self.items_table.grid(row=0, column=0, padx=[22, 20], pady=[20, 20])

        self.button_frame = tk.LabelFrame(self.root, bg="#7575a3", font=(
            'Georgia', 13, 'bold'))
        self.button_frame.place(x=1180, y=100)

        self.showBill_but = tk.Button(self.button_frame, text="Show Bills", width=15, font=(
            'Georgia', 11, 'bold'), bg='#656554', fg='black', height=3, command=self.show_bills)
        self.showBill_but.grid(row=0, column=0, padx=[10, 10], pady=[42,20])

        self.showBill_but = tk.Button(self.button_frame, text="Store Data", width=15, font=(
            'Georgia', 11, 'bold'), bg='#656554', fg='black', height=3, command=self.data_store)
        self.showBill_but.grid(row=1, column=0, padx=[10, 10], pady=[20,20])

        self.showBill_but = tk.Button(self.button_frame, text="Calculator", width=15, font=(
            'Georgia', 11, 'bold'), bg='#656554', fg='black', height=3, command=self.calculator)
        self.showBill_but.grid(row=2, column=0, padx=[10, 10], pady=[20,20])

        self.showBill_but = tk.Button(self.button_frame, text="Store", width=15, font=(
            'Georgia', 11, 'bold'), bg='#656554', fg='black', height=3, command=self.add_product_window)
        self.showBill_but.grid(row=3, column=0, padx=[10, 10], pady=[20,20])

        self.showBill_but = tk.Button(self.button_frame, text="Reports", width=15, font=(
            'Georgia', 11, 'bold'), bg='#656554', fg='black', height=3, command=self.reports)
        self.showBill_but.grid(row=4, column=0, padx=[10, 10], pady=[20,42])

        # Create an empty cart list to store the selected items
        self.cart_list = []

        # Fetch and update product list in combobox
        self.update_product_combobox()