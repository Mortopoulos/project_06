import sqlite3
import re
from tkinter import messagebox


class ClientManager:
    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()
        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS clients (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            first_name TEXT,
                            last_name TEXT,
                            phone TEXT,
                            email TEXT)"""
        )
        self.conn.commit()

    def is_valid_email(self, email):
        email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
        return re.fullmatch(email_regex, email) is not None

    def is_valid_phone(self, phone):
        phone_regex = r'^\d{10}$'
        return re.fullmatch(phone_regex, phone) is not None

    def client_exists(self, phone, email):
        self.cursor.execute(
            "SELECT * FROM clients WHERE phone = ? OR email = ?",
            (phone, email),
        )
        return self.cursor.fetchone() is not None

    def add_client(self, first_name, last_name, phone, email):
        if not self.is_valid_email(email) or not self.is_valid_phone(phone):
            messagebox.showerror("Μη έγκυρο email ή αριθμός τηλεφώνου", "Παρακαλώ εισάγετε έγκυρα στοιχεία.")
            return

        if self.client_exists(phone, email):
            messagebox.showerror("Ο πελάτης υπάρχει ήδη", "Παρακαλώ δοκιμάστε ξανά.")
            return

        self.cursor.execute(
            "INSERT INTO clients (first_name, last_name, phone, email) VALUES (?, ?, ?, ?)",
            (first_name, last_name, phone, email),
        )
        self.conn.commit()

    def delete_client(self, id):
        self.cursor.execute("DELETE FROM clients WHERE id=?", (id,))
        self.conn.commit()

    def search_clients(self, search_term):
        self.cursor.execute(
            "SELECT * FROM clients WHERE first_name LIKE ? OR last_name LIKE ? OR phone LIKE ? OR email LIKE ?",
            (
                f"%{search_term}%",
                f"%{search_term}%",
                f"%{search_term}%",
                f"%{search_term }%",
            ),
        )
        return self.cursor.fetchall()

    def update_client(
        self, id, first_name=None, last_name=None, phone=None, email=None
    ):
        updates = {}
        if first_name:
            updates["first_name"] = first_name
        if last_name:
            updates["last_name"] = last_name
        if phone:
            updates["phone"] = phone
        if email:
            updates["email"] = email
        update_query = ", ".join([f"{key}=?" for key in updates.keys()])
        update_values = tuple(updates.values()) + (id,)
        self.cursor.execute(
            f"UPDATE clients SET {update_query} WHERE id=?", update_values
        )
        self.conn.commit()

    def get_all_clients(self):
        self.cursor.execute("SELECT * FROM clients")
        return self.cursor.fetchall()

    def search_clients_by_number(self, number_input):
        self.cursor.execute(f"SELECT * FROM clients WHERE phone LIKE '{number_input}%'")
        return self.cursor.fetchall()

    def get_client(self, client_id):
        all_clients = self.get_all_clients()
        return [client for client in all_clients if client[0] == client_id][0]

    def __del__(self):
        self.conn.close()
