from client_manager import ClientManager
from appointment_manager import AppointmentManager

import os
import smtplib
from datetime import datetime
from email.mime.text import MIMEText

from openpyxl import Workbook
from openpyxl.styles import Font
from openpyxl.styles.colors import Color
from openpyxl.styles.fills import PatternFill
from openpyxl.utils import get_column_letter


def export_all_appointments_to_xlsx(
    appointment_manager, client_manager, destination_folder_path
):
    wb = Workbook()
    sheet = wb.active

    headings = ["ID", "Client", "Email", "Phone", "Name", "Date", "Time (Minutes)"]
    for col_num, heading in enumerate(headings, 1):
        col_letter = get_column_letter(col_num)
        cell = sheet[f"{col_letter}1"]
        cell.value = heading
        cell.font = Font(bold=True)
        cell.fill = PatternFill(patternType="solid", fgColor=Color(rgb="C6EFCE"))

    appointments = appointment_manager.get_all_appointments()
    # (id , name , date , time , client_id )
    for row_num, appointment in enumerate(appointments, 2):
        client = client_manager.get_client(appointment[4])
        # (id, name, phone, email)
        sheet[f"A{row_num}"] = appointment[0]
        sheet[f"B{row_num}"] = client[1]
        sheet[f"C{row_num}"] = client[3]
        sheet[f"D{row_num}"] = client[2]
        sheet[f"E{row_num}"] = appointment[1]
        sheet[f"F{row_num}"] = appointment[2]
        sheet[f"G{row_num}"] = appointment[3]

    filename = "appointments.xlsx"
    filepath = os.path.join(destination_folder_path, filename)
    wb.save(filepath)
    return filepath


def send_reminders_to_clients_at_date(
    appointment_manager,
    client_manager,
    date,
    email="dr.georgepapadopoulos@gmail.com",
    pass_code="sphgkfocygdxfneu",
):
    smtp_server = smtplib.SMTP("smtp.gmail.com", 587)
    smtp_server.starttls()
    # smtp_server.login('dr.georgepapadopoulos@gmail.com', 'sphgkfocygdxfneu')
    smtp_server.login(email, pass_code)

    for appointment in appointment_manager.get_appointments_on_date(date):
        date = datetime.strptime(appointment[2], "%Y-%m-%d %H:%M:%S")
        import locale

        locale.setlocale(locale.LC_TIME, "el_GR")
        date_time = date.strftime("%A, %d-%b-%Y, %H:%M:%S")
        client = client_manager.get_client(appointment[4])
        message = MIMEText(
            f"Αγαπητέ/ή {client[1]},\n\nΑυτή είναι μια φιλική υπενθύμιση ότι έχετε ραντεβού μαζί μας στις {date_time}.\nΠαρακαλούμε, ενημερώστε μας εκ των προτέρων εαν χρειαστεί να αναπρογραμματίσετε ή να ακυρώσετε το ραντεβού σας.\n\nΜε τους θερμότερους χαιρετισμούς,\n\nΗ ομάδα του SchedulEase."
        )
        message["Subject"] = "Υπενθύμιση ραντεβού"
        message["From"] = "dr.georgepapadopoulos@gmail.com"
        # message['From'] = email
        message["To"] = client[3]

        smtp_server.sendmail(
            "dr.georgepapadopoulos@gmail.com", client[3], message.as_string()
        )
        # smtp_server.sendmail(email, client[3], message.as_string())

    smtp_server.quit()
