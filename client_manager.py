import sqlite3


class ClientManager:
    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()
        self.cursor.execute(
            'CREATE TABLE IF NOT EXISTS clients (id TEXT, name TEXT, phone TEXT, email TEXT)'
        )
        self.conn.commit()

    def add_client(self, id, name, phone, email):
        self.cursor.execute(
            'INSERT INTO clients VALUES (?, ?, ?, ?)', (id, name, phone, email)
        )
        self.conn.commit()

    # Προσθέτει ψεύτικους χρήστες
    def add_test_clients(self):
        clients = [
            (1, 'user1', 123, '1@gmail'),
            (2, 'user2', 124, '2@gmail'),
            (3, 'user3', 125, '3@gmail'),
            (4, 'user4', 126, '4@gmail'),
        ]
        for c in clients:
            self.add_client(*c)

    def delete_client(self, id):
        self.cursor.execute('DELETE FROM clients WHERE id=?', (id,))
        self.conn.commit()

    def get_all_clients(self):
        self.cursor.execute('SELECT * FROM clients')
        return self.cursor.fetchall()

    def __del__(self):
        self.conn.close()
