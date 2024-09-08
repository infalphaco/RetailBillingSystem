import sqlite3
from sqlite3 import Error

class Connection:
    
    def __init__(self, db_file):
        self.conn = None
        self.cursor = None
        try:
            self.conn = sqlite3.connect(db_file, detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
            self.cursor = self.conn.cursor()
            print(f"SQLite version: {sqlite3.version}")
            self.create_database_tables()
        except Error as e:
            print(f"Error connecting to database: {e}")
    
    def create_database_tables(self):
        if not self.cursor:
            print("No database connection.")
            return

        try:
            self.cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                                        fullname TEXT NOT NULL,
                                        username TEXT NOT NULL,
                                        password TEXT NOT NULL,
                                        category TEXT NOT NULL,
                                        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                                    )''')

            self.cursor.execute('''CREATE TABLE IF NOT EXISTS bills (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                bill_number TEXT NOT NULL,
                                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                                total_amount REAL NOT NULL
                            )''')

            self.cursor.execute('''CREATE TABLE IF NOT EXISTS bill_items (
                                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                                        bill_id INTEGER NOT NULL,
                                        product_id INTEGER NOT NULL,
                                        quantity INTEGER NOT NULL,
                                        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                                        FOREIGN KEY (bill_id) REFERENCES bills(id),
                                        FOREIGN KEY (product_id) REFERENCES csv_data(id)
                                    )''')

            self.cursor.execute('''CREATE TABLE IF NOT EXISTS csv_data (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                item_name TEXT,
                                unit_price REAL,
                                stock INTEGER,
                                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                            )''')

            self.cursor.execute('''CREATE TABLE IF NOT EXISTS login_history (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                user_id INTEGER NOT NULL,
                                full_name TEXT,
                                login_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                                FOREIGN KEY (user_id) REFERENCES users(id)
                            )''')

            self.conn.commit()
        except Error as e:
            print(f"Error creating tables: {e}")

# Example usage
if __name__ == "__main__":
    db_connection = Connection("db/retail_billing.db")