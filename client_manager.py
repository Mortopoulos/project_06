import sqlite3


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

    def add_client(self, first_name, last_name, phone, email):
        self.cursor.execute(
            "INSERT INTO clients (first_name, last_name, phone, email) VALUES (?, ?, ?, ?)",
            (first_name, last_name, phone, email),
        )
        self.conn.commit()

    def delete_client(self, id):
        self.cursor.execute("DELETE FROM clients WHERE id=?", (id,))
        self.conn.commit()

    def search_client(self):
        pass

    def update_client(self):
        pass

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
