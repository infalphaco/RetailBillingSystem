import tkinter as tk
from tkinter import messagebox, ttk, filedialog
import sqlite3
import openpyxl

class BillReport:
    def __init__(self, root):
        self.root = root
        self.root.title("FIREFIX RETAIL BILLING SYSTEM | Select Report")
        self.root.resizable(False, False)
        self.root['bg'] = '#a7a5cc'

        # Get the screen width and height
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Calculate the x and y coordinates to center the window
        x = (screen_width - 600) // 2
        y = (screen_height - 300) // 2

        # Set the window position
        self.root.geometry(f'600x300+{x}+{y}')

        # Create and connect to the database
        self.conn = sqlite3.connect("db/retail_billing.db")
        self.cursor = self.conn.cursor()

        # Create labels and inputs for date and time range selection
        start_date_label = tk.Label(self.root, text="Start Date (YYYY-MM-DD):", bg='#a7a5cc')
        start_date_label.pack(pady=5)
        self.start_date_entry = tk.Entry(self.root)
        self.start_date_entry.pack(pady=5)

        start_time_label = tk.Label(self.root, text="Start Time (HH:MM):", bg='#a7a5cc')
        start_time_label.pack(pady=5)
        self.start_time_entry = tk.Entry(self.root)
        self.start_time_entry.pack(pady=5)

        end_date_label = tk.Label(self.root, text="End Date (YYYY-MM-DD):", bg='#a7a5cc')
        end_date_label.pack(pady=5)
        self.end_date_entry = tk.Entry(self.root)
        self.end_date_entry.pack(pady=5)

        end_time_label = tk.Label(self.root, text="End Time (HH:MM):", bg='#a7a5cc')
        end_time_label.pack(pady=5)
        self.end_time_entry = tk.Entry(self.root)
        self.end_time_entry.pack(pady=5)

        # Create a button to confirm the selection
        select_button = tk.Button(self.root, text="Select", command=self.select_date_range)
        select_button.pack(pady=20)

    def select_date_range(self):
        start_date = self.start_date_entry.get()
        start_time = self.start_time_entry.get()
        end_date = self.end_date_entry.get()
        end_time = self.end_time_entry.get()
        
        if not start_date or not start_time or not end_date or not end_time:
            messagebox.showerror("Invalid Input", "Please enter valid date and time range.")
            return

        start_datetime = f"{start_date} {start_time}:00"
        end_datetime = f"{end_date} {end_time}:00"
        
        self.export_bills_to_excel(start_datetime, end_datetime)

    def export_bills_to_excel(self, start_datetime, end_datetime):
        try:
            self.cursor.execute("SELECT * FROM bills WHERE timestamp BETWEEN ? AND ?", (start_datetime, end_datetime))
            bills_data = self.cursor.fetchall()

            if not bills_data:
                messagebox.showinfo("No Data", "No bills found for the selected date and time range.")
                return

            file_path = filedialog.asksaveasfilename(defaultextension=".xlsx",
                                                     filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")])
            if not file_path:
                return

            workbook = openpyxl.Workbook()
            sheet = workbook.active
            sheet.title = "Bills"

            headers = ["ID", "Bill Number", "Timestamp", "Total Amount"]
            sheet.append(headers)

            for row in bills_data:
                sheet.append(row)

            workbook.save(file_path)
            messagebox.showinfo("Success", f"Bills data has been exported to {file_path}")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to export data: {e}")
