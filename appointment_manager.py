import sqlite3
from datetime import datetime, timedelta


class AppointmentManager:
    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS appointments (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, date DATETIME, duration INTEGER, client_id INTEGER, employee_id INTEGER)"
        )
        self.conn.commit()

    def add_appointment(self, name, date, duration, client_id, employee_id):
        overlapping_appointments = self.get_overlapping_appointments(date, duration)
        if overlapping_appointments:
            raise ValueError(
                f"We have overlapping appointments:{overlapping_appointments}"
            )

        self.cursor.execute(
            "INSERT INTO appointments (name, date, duration, client_id, employee_id) VALUES (?, ?, ?, ?, ?)",
            (name, date, duration, client_id, employee_id),
        )
        self.conn.commit()

    def delete_appointment(self, appointment_id):
        self.cursor.execute("DELETE FROM appointments WHERE id=?", (appointment_id))
        self.conn.commit()

    def get_all_appointments(self):
        self.cursor.execute("SELECT * FROM appointments")
        return self.cursor.fetchall()

    def get_appointment(self, appointment_id):
        self.cursor.execute(
            "SELECT * FROM appointments WHERE appointment_id = ?", (appointment_id,)
        )
        return self.cursor.fetchone()

    def edit_appointment(
        self, appointment_id, name, date, duration, client_id, employee_id
    ):
        self.cursor.execute(
            "UPDATE appointments SET name=?, date=?, duration=?, client_id=?, employee_id=? WHERE id=?",
            (name, date, duration, client_id, employee_id, appointment_id),
        )
        self.conn.commit()

    def get_appointments_on_date(self, date):
        self.cursor.execute(
            "SELECT * FROM appointments WHERE DATE(date)=DATE(?)", (date,)
        )
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
        self, start_time, duration, exception_appointment_id=None
    ):
        end_time = start_time + timedelta(minutes=duration)
        if exception_appointment_id is None:
            self.cursor.execute(
                "SELECT * FROM appointments WHERE date < ? AND datetime(date, '+' || ? || ' minutes') > ?",
                (end_time, duration, start_time),
            )
        else:
            self.cursor.execute(
                "SELECT * FROM appointments WHERE date < ? AND datetime(date, '+' || ? || ' minutes') > ? AND id != ?",
                (end_time, duration, start_time, exception_appointment_id),
            )
        overlapping_appointments = self.cursor.fetchall()
        return overlapping_appointments
