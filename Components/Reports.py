import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
import sqlite3
import tkinter as sys
import os
from ReportList.Bill_report import BillReport
from ReportList.Store_data_list_report import StoreDataList
from ReportList.Billed_item_list_report import BilledItemList

class Reports:
    def __init__(self, root):
        self.root = root
        self.root.title("FIREFIX RETAIL BILLING SYSTEM|Store Panel")
        self.root.resizable(False, False)
        self.root['bg'] = '#a7a5cc'
        # icon_path = self.resource_path("img/icon.ico")
        # self.root.iconbitmap(icon_path)

        # Get the screen width and height
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Calculate the x and y coordinates to center the window
        x = (screen_width - 590) // 2
        y = (screen_height - 120) // 2

        # Set the window position
        self.root.geometry(f'590x120+{x}+{y}')

        # Create and connect to the database
        self.conn = sqlite3.connect("db/retail_billing.db")
        self.cursor = self.conn.cursor()

        self.button_frame = tk.LabelFrame(self.root, bg="#7575a3")
        self.button_frame.place(x=20, y=10)

        self.bill_button  = tk.Button(self.button_frame, text="Bill Report" , bg='#656554', width=15, font=(
            'Georgia', 11, 'bold'), fg="black", height=3, command=self.billReport)
        self.bill_button.grid(row=0, column=0, padx=[10,10], pady=[10,10])

        self.product_button  = tk.Button(self.button_frame, text="Store Data List" , bg='#656554', width=15, font=(
            'Georgia', 11, 'bold'), fg="black", height=3, command=self.storeDataList)
        self.product_button.grid(row=0, column=2, padx=[10,10], pady=[10,10])

        self.product_button  = tk.Button(self.button_frame, text="Billed items" , bg='#656554', width=15, font=(
            'Georgia', 11, 'bold'), fg="black", height=3, command=self.billedItem)
        self.product_button.grid(row=0, column=3, padx=[10,10], pady=[10,10])

    def billReport(self):
            billreport_window = tk.Toplevel(self.root)
            bilreport_app = BillReport(billreport_window)

    def billedItem(self):
            billeditemreport_window = tk.Toplevel(self.root)
            billeditem_app = BilledItemList(billeditemreport_window)

    def storeDataList(self):
            StoreData_window = tk.Toplevel(self.root)
            storeDataList_app = StoreDataList(StoreData_window)
