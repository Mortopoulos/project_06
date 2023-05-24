import sqlite3
from datetime import timedelta

# Add all of the necessary imports


class AppointmentManager:
    def __init__(self, db_file):
        # Connect to the SQLite database
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()

        # Create the 'appointments' table if it doesn't exist
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS appointments (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, date DATETIME, duration INTEGER, client_id INTEGER, employee_id INTEGER)"
        )

        # Commit the changes to the database
        self.conn.commit()

    def add_appointment(self, name, date, duration, client_id, employee_id):
        # Check for overlapping appointments
        overlapping_appointments = self.get_overlapping_appointments(
            date, duration, employee_id
        )
        if overlapping_appointments:
            raise ValueError(
                f"We have overlapping appointments: {overlapping_appointments}"
            )

        # Insert the new appointment into the 'appointments' table

        self.cursor.execute(
            "INSERT INTO appointments (name, date, duration, client_id, employee_id) VALUES (?, ?, ?, ?, ?)",
            (name, date, duration, client_id, employee_id),
        )

        # Commit the changes to the database
        self.conn.commit()

    def delete_appointment(self, appointment_id):
        # Delete an appointment from the 'appointments' table based on the appointment ID
        self.cursor.execute("DELETE FROM appointments WHERE id=?", (appointment_id,))

        # Commit the changes to the database
        self.conn.commit()

    def get_all_appointments(self):
        # Retrieve all appointments from the 'appointments' table
        self.cursor.execute("SELECT * FROM appointments")

        # Return the fetched appointments
        return self.cursor.fetchall()

    def get_appointment(self, appointment_id):
        # Retrieve an appointment from the 'appointments' table based on the appointment ID
        self.cursor.execute("SELECT * FROM appointments WHERE id=?", (appointment_id,))

        # Return the fetched appointment
        return self.cursor.fetchone()

    def update_appointment(
        self, appointment_id, name, date, duration, client_id, employee_id
    ):
        # Check for overlapping appointments
        overlapping_appointments = self.get_overlapping_appointments(
            date, duration, employee_id, appointment_id
        )
        if overlapping_appointments:
            raise ValueError(
                f"We have overlapping appointments: {overlapping_appointments}"
            )

        # Update an appointment in the 'appointments' table based on the appointment ID

        self.cursor.execute(
            "UPDATE appointments SET name=?, date=?, duration=?, client_id=?, employee_id=? WHERE id=?",
            (name, date, duration, client_id, employee_id, appointment_id),
        )

        # Commit the changes to the database
        self.conn.commit()

    def search_appointments(self, search_term):
        self.cursor.execute(
            "SELECT * FROM appointments WHERE id LIKE ? OR name LIKE ? OR date LIKE ? OR duration LIKE ? OR client_id LIKE ? OR employee_id LIKE ?",
            (
                f"%{search_term}%",
                f"%{search_term}%",
                f"%{search_term}%",
                f"%{search_term}%",
                f"%{search_term}%",
                f"%{search_term}%",
            ),
        )
        return self.cursor.fetchall()

    def get_appointments_on_date(self, date):
        # Retrieve appointments from the 'appointments' table for a specific date
        self.cursor.execute(
            f"SELECT * FROM appointments WHERE date LIKE '{date}%';"
        )

        # Return the fetched appointments
        return self.cursor.fetchall()

    def get_appointments_for_client(self, client_id):
        self.cursor.execute(
            "SELECT * FROM appointments WHERE client_id=?", (client_id,)
        )
        return self.cursor.fetchall()

    def get_appointments_for_client_on_date(self, client_id, date):
        self.cursor.execute(
            "SELECT * FROM appointments WHERE client_id=? AND DATE(date)=DATE(?)",
            (client_id, date),
        )
        return self.cursor.fetchall()

    def get_appointments_for_employee(self, employee_id):
        self.cursor.execute(
            "SELECT * FROM appointments WHERE employee_id=?", (employee_id,)
        )
        return self.cursor.fetchall()

    def __del__(self):
        self.conn.close()

    def get_overlapping_appointments(
        self, start_time, duration, employee_id, exception_appointment_id=None
    ):
        end_time = start_time + timedelta(minutes=duration)

        if exception_appointment_id is None:
            # Retrieve appointments that have a start time earlier than the end time of the current appointment or an end time later than the start time of the current appointment for the same employee

            self.cursor.execute(
                "SELECT * FROM appointments WHERE (date < ? AND (date > ? OR (datetime(date, '+' || duration || ' minutes') > ?)) AND employee_id = ?)",
                (end_time, start_time, start_time, employee_id),
            )

        else:
            # Retrieve appointments that have a start time earlier than the end time of the current appointment or an end time later than the start time of the current appointment for the same employee, excluding the appointment with the specified exception_appointment_id
            self.cursor.execute(
                "SELECT * FROM appointments WHERE (date < ? AND (date > ? OR (datetime(date, '+' || duration || ' minutes') > ?)) AND employee_id = ? AND id != ?)",
                (
                    end_time,
                    start_time,
                    start_time,
                    employee_id,
                    exception_appointment_id,
                ),
            )

        # Fetch the overlapping appointments
        overlapping_appointments = self.cursor.fetchall()

        # Return the fetched overlapping appointments
        return overlapping_appointments
