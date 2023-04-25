import sqlite3


class AppointmentManager:
    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()
        self.cursor.execute(
            'CREATE TABLE IF NOT EXISTS appointments (id TEXT, name TEXT, date DATETIME, time TEXT, client_id TEXT)'
        )
        self.conn.commit()

    def add_appointment(self, appointment_id, name, date, time, client_id):
        self.cursor.execute(
            'INSERT INTO appointments VALUES (?, ?, ?, ?, ?)', (appointment_id, name, date, time, client_id)
        )
        self.conn.commit()

    # Προσθέτει ψεύτικους χρήστες
    # def add_test_appointments(self):
    #     appointments = [
    #         (1, 'user1', 123, '1@gmail'),
    #         (2, 'user2', 124, '2@gmail'),
    #         (3, 'user3', 125, '3@gmail'),
    #         (4, 'user4', 126, '4@gmail'),
    #     ]
    #     for c in appointments:
    #         self.add_client(*c)

    def delete_appointment(self, appointment_id):
        self.cursor.execute('DELETE FROM appointments WHERE id=?', (appointment_id))
        self.conn.commit()

    def get_all_appointments(self):
        self.cursor.execute('SELECT * FROM appointments')
        return self.cursor.fetchall()



    def get_appointment(self, appointment_id):
        all_appointments = self.get_all_appointments() 
        return [appointment for appointment in all_appointments if appointment[0] == appointment_id][0]


    def edit_appointment(self, appointment_id, name, date, time, client_id):
        self.cursor.execute(
            'UPDATE appointments SET name=?, date=?, time=?, client_id=? WHERE id=?',
            (name, date, time, client_id, appointment_id)
        )
        self.conn.commit()


    def get_appointments_on_date(self, date):
        self.cursor.execute('SELECT * FROM appointments WHERE DATE(date)=DATE(?)', (date,))
        return self.cursor.fetchall()



    def get_appointments_for_client(self, client_id):
        self.cursor.execute('SELECT * FROM appointments WHERE client_id=?', (client_id,))
        return self.cursor.fetchall()

    def get_appointments_for_client_on_date(self, client_id, date):
        self.cursor.execute('SELECT * FROM appointments WHERE client_id=? AND DATE(date)=DATE(?)', (client_id, date))
        return self.cursor.fetchall()


    

    def __del__(self):
        self.conn.close()
