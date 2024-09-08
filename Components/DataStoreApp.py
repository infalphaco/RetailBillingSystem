import tkinter as tk
from tkinter import messagebox, filedialog
import sqlite3
import csv
import sys
import os

class DataStoreApp:
    def __init__(self, root):
        self.root = root
        self.root['bg'] = "#a7a5cc"
        self.root.resizable(False, False)
        self.root.title("CSV Uploader")
        
         # Get the screen width and height
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Calculate the x and y coordinates to center the window
        x = (screen_width - 600) // 2
        y = (screen_height - 200) // 2

        # Set the window position
        self.root.geometry(f'600x200+{x}+{y}')

        self.frame = tk.Frame(root)
        self.frame.pack(pady=20)

        label_filepath = tk.Label(self.frame, text="File Path:")
        label_filepath.grid(row=0, column=0, padx=5, pady=5)

        self.entry_filepath = tk.Entry(self.frame, width=50)
        self.entry_filepath.grid(row=0, column=1, padx=5, pady=5)

        button_browse = tk.Button(self.frame, text="Browse", command=self.select_file, font=(
            'Georgia', 11, 'bold'))
        button_browse.grid(row=0, column=2, padx=5, pady=5)

        upload_button = tk.Button(root, text="Upload CSV", command=self.upload_csv, bg="blue", font=(
            'Georgia', 12, 'bold'))
        upload_button.pack()

    def resource_path(self, relative_path):
        """ Get absolute path to resource, works for dev and for PyInstaller """
        if getattr(sys, 'frozen', False):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)
        
    def select_file(self):
        filepath = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if filepath:
            self.entry_filepath.delete(0, tk.END)
            self.entry_filepath.insert(tk.END, filepath)

    def upload_csv(self):
        filepath = self.entry_filepath.get()
        if not filepath:
            messagebox.showerror("Error", "Please select a CSV file.")
            return
        try:
            with open(filepath, newline='') as csvfile:
                csvreader = csv.DictReader(csvfile)
                self.store_in_database(csvreader)
                messagebox.showinfo("Success", "Data has been uploaded and stored in the database.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def store_in_database(self, csvreader):
        conn = sqlite3.connect("db/retail_billing.db")
        cursor = conn.cursor()       

        for row in csvreader:
            cursor.execute('''SELECT id FROM csv_data WHERE item_name = ?''', (row['Item name'],))
            existing_item = cursor.fetchone()
            if existing_item:
                # Update the existing record
                cursor.execute('''UPDATE csv_data 
                                  SET unit_price = ?, stock = ? 
                                  WHERE id = ?''',
                               (row['Unit price'], row['Stock'], existing_item[0]))
            else:
                # Insert the new record
                cursor.execute('''INSERT INTO csv_data (item_name, unit_price, stock) 
                                  VALUES (?, ?, ?)''', (row['Item name'], row['Unit price'], row['Stock']))
        
        conn.commit()
        conn.close()