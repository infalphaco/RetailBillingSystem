import tkinter as tk
import os
import tkinter as sys

class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("FIREFIX RETAIL BILLING SYSTEM|Store Panel")
        self.root.resizable(False, False)
        self.root['bg'] = '#a7a5cc'
        # icon_path = self.resource_path("img/icon.ico")
        # self.root.iconbitmap(icon_path)

        # Entry widget to display input/output
        self.entry = tk.Entry(root, width=30, borderwidth=5, font=('Georgia', 15))
        self.entry.grid(row=0, column=0, columnspan=4, padx=10, pady=10)

        # "=" button
        equal_button = tk.Button(root, text='=', padx=10, pady=10, command=self.calculate, font=('Georgia', 20, 'bold'))
        equal_button.grid(row=4, column=2)

        # Define buttons
        buttons = [
            ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('/', 1, 3),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('*', 2, 3),
            ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('-', 3, 3),
            ('0', 4, 0), ('.', 4, 1), ('+', 4, 3)
        ]

        # Create buttons and assign them to the grid
        for (text, row, col) in buttons:
            button = tk.Button(root, text=text, padx=10, pady=10, command=lambda char=text: self.button_click(char), font=('Georgia', 20, 'bold'))
            button.grid(row=row, column=col, pady=10)

        # Clear button
        clear_button = tk.Button(root, text='C', padx=10, pady=10, command=self.clear, width=18, font=('Georgia', 20, 'bold'))
        clear_button.grid(row=5, column=0, columnspan=5, pady=10)

        # Bind keyboard events
        self.root.bind("<Key>", self.key_pressed)

    def resource_path(self, relative_path):
        """ Get absolute path to resource, works for dev and for PyInstaller """
        if getattr(sys, 'frozen', False):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)

    # Function to perform arithmetic operation
    def calculate(self):
        try:
            expression = self.entry.get()
            print("Calculating:", expression)  # Print expression being evaluated
            result = eval(expression)
            self.entry.delete(0, tk.END)
            self.entry.insert(tk.END, str(result))
        except Exception as e:
            self.entry.delete(0, tk.END)
            self.entry.insert(tk.END, "Error: " + str(e))

    # Function to append clicked buttons to entry widget
    def button_click(self, char):
        current = self.entry.get()
        self.entry.delete(0, tk.END)
        self.entry.insert(tk.END, current + char)

    # Function to clear the entry widget
    def clear(self):
        self.entry.delete(0, tk.END)

    # Function to handle key presses
    def key_pressed(self, event):
        key = event.char
        if key in '0123456789+-*/.':
            current = self.entry.get()
            self.entry.delete(0, tk.END)
            self.entry.insert(tk.END, current + key)
        elif key == '\r':  # Enter key
            self.calculate()
        elif key == '\x08':  # Backspace key
            current = self.entry.get()
            self.entry.delete(0, tk.END)
            self.entry.insert(tk.END, current[:-1])
        elif key == 'c' or key == 'C':
            self.clear()

if __name__ == "__main__":
    root = tk.Tk()
    app = Calculator(root)
    root.mainloop()