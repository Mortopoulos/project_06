import sqlite3

# Add all of the necessary imports


class EmployeeManager:
    def __init__(self, db_file):
        # Connect to the SQLite database
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()

        # Create the 'employees' table if it doesn't exist
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS employees (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, phone TEXT, email TEXT, pass_code TEXT)"
        )

        # Commit the changes to the database
        self.conn.commit()

    def add_employee(self, name, phone, email, pass_code):
        # Insert a new employee into the 'employees' table
        self.cursor.execute(
            "INSERT INTO employees (name, phone, email, pass_code) VALUES (?, ?, ?, ?)",
            (name, phone, email, pass_code),
        )

        # Commit the changes to the database
        self.conn.commit()

    def delete_employee(self, id):
        # Delete an employee from the 'employees' table based on the employee ID
        self.cursor.execute("DELETE FROM employees WHERE id=?", (id,))

        # Commit the changes to the database
        self.conn.commit()

    def search_employee(self, search_term):
        # Search for employees in the 'employees' table based on a search term
        self.cursor.execute(
            "SELECT * FROM employees WHERE name LIKE ? OR phone LIKE ? OR email LIKE ? OR pass_code LIKE ?",
            (
                f"%{search_term}%",
                f"%{search_term}%",
                f"%{search_term}%",
                f"%{search_term}%",
            ),
        )

        # Return the fetched employees
        return self.cursor.fetchall()

    def update_employee(self, name=None, phone=None, email=None, pass_code=None):
        # Update an employee's information in the 'employees' table
        updates = {}
        if name:
            updates["name"] = name
        if phone:
            updates["phone"] = phone
        if email:
            updates["email"] = email
        if pass_code:
            updates["pass_code"] = pass_code
        update_query = ", ".join([f"{key}=?" for key in updates.keys()])
        update_values = tuple(updates.values()) + (id,)
        self.cursor.execute(
            f"UPDATE employee SET {update_query} WHERE id=?", update_values
        )

        # Commit the changes to the database
        self.conn.commit()

    def get_all_employees(self):
        # Retrieve all employees from the 'employees' table
        self.cursor.execute("SELECT * FROM employees")

        # Return the fetched employees
        return self.cursor.fetchall()

    def get_employee(self, employee_id):
        # Retrieve an employee from the 'employees' table based on the employee ID
        query = "SELECT * FROM employees WHERE id = ?"
        self.cursor.execute(query, (employee_id))

        # Return the fetched employee
        return self.cursor.fetchone()

    def __del__(self):
        # Close the database connection when the object is deleted
        self.conn.close()
