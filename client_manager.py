import sqlite3


class ClientManager:
    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()
        self.cursor.execute(
            'CREATE TABLE IF NOT EXISTS clients (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, phone TEXT, email TEXT)'
        )
        self.conn.commit()

    def add_client(self, name, phone, email):
        self.cursor.execute(
            'INSERT INTO clients (name, phone, email) VALUES (?, ?, ?)', (name, phone, email)
        )
        self.conn.commit()
        

    # Προσθέτει ψεύτικους χρήστες
    def add_test_clients(self):
        clients = [
            ('user1', 123, '1@gmail'),
            ('user2', 124, '2@gmail'),
            ('user3', 125, '3@gmail'),
            ('user4', 126, '4@gmail'),
        ]
        for c in clients:
            self.add_client(*c)

    def delete_client(self, id):
        self.cursor.execute('DELETE FROM clients WHERE id=?', (id,))
        self.conn.commit()

    def get_all_clients(self):
        self.cursor.execute('SELECT * FROM clients')
        return self.cursor.fetchall()

    def search_clients_by_number(self, number_input):
        self.cursor.execute(f"SELECT * FROM clients WHERE phone LIKE '{number_input}%'")
        return self.cursor.fetchall()

    def get_client(self, client_id):
        all_clients = self.get_all_clients() 
        return [client for client in all_clients if client[0] == client_id][0]
    
    def __del__(self):
        self.conn.close()
