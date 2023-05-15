import sqlite3


class ClientManager:
    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()
        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS clients (
                            id INTEGER PRIMARY KEY,
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

    def search_client(self, search_term):
        self.cursor.execute(
            "SELECT * FROM clients WHERE first_name LIKE ? OR last_name LIKE ? OR phone LIKE ? OR email LIKE ?",
            (f"%{search_term}%", f"%{search_term}%", f"%{search_term}%", f"%{search_term }%"),
        )
        return self.cursor.fetchall()

    def update_client(self, id, first_name=None, last_name=None, phone=None, email=None):
        updates = {}
        if first_name:
            updates['first_name'] = first_name
        if last_name:
            updates['last_name'] = last_name
        if phone:
            updates['phone'] = phone
        if email:
            updates['email'] = email
        update_query = ", ".join([f"{key}=?" for key in updates.keys()])
        update_values = tuple(updates.values()) + (id,)
        self.cursor.execute(f"UPDATE clients SET {update_query} WHERE id=?", update_values)
        self.conn.commit()


#    def update_client(self, id, first_name=None, last_name=None, phone=None, email=None):
#        update_clause = []
#        if first_name:
#            update_clause.append(f"first_name='{first_name}'")
#        if last_name:
#            update_clause.append(f"last_name='{last_name}'")
#        if phone:
#            update_clause.append(f"phone='{phone}'")
#        if email:
#            update_clause.append(f"email='{email}'")
#            set_clause = ", ".join(update_clause)
#        self.cursor.execute(f"UPDATE clients SET {set_clause} WHERE id=?", (id,))
#        self.conn.commit()

    def get_all_clients(self):
        self.cursor.execute("SELECT * FROM clients")
        return self.cursor.fetchall()

    def get_client(self, client_id):
        all_clients = self.get_all_clients()
        return [client for client in all_clients if client[0] == client_id][0]

    def __del__(self):
        self.conn.close()
