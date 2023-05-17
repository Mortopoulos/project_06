import sqlite3


class EmployeeManager:
    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS employees (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, phone TEXT, email TEXT, pass_code TEXT)"
        )
        self.conn.commit()

    def add_employee(self, name, phone, email, pass_code):
        self.cursor.execute(
            "INSERT INTO employees (name, phone, email, pass_code) VALUES (?, ?, ?, ?)",
            (name, phone, email, pass_code),
        )
        self.conn.commit()

    def delete_employee(self, id):
        self.cursor.execute("DELETE FROM employees WHERE id=?", (id,))
        self.conn.commit()

    def get_all_employees(self):
        self.cursor.execute("SELECT * FROM employees")
        return self.cursor.fetchall()

    def get_employee(self, employee_id):
        query = "SELECT * FROM employees WHERE id = ?"
        result = self.connection.execute(query, (employee_id,))
        return result.fetchone()

    def __del__(self):
        self.conn.close()
