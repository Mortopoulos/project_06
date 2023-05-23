import tkinter as tk
from datetime import datetime
from tkinter import StringVar, ttk

from tkcalendar import DateEntry

from appointment_manager import AppointmentManager
from client_manager import ClientManager
from employee_manager import EmployeeManager

from utils import export_all_appointments_to_xlsx

DATABASE_FILE = "app.db"


class Appointments:
    def __init__(self, tab):
        self.appointment_manager = AppointmentManager(DATABASE_FILE)
        self.employee_manager = EmployeeManager(DATABASE_FILE)
        self.client_manager = ClientManager(DATABASE_FILE)
        self.tab = tab
        self.curselection = 0
        self.search_terms = StringVar()
        self.search_terms.trace("w", lambda *args: self.search_appointments())
        self.tab.grid_rowconfigure(0, weight=1)
        self.tab.grid_columnconfigure(0, weight=1)
        self.tab.grid_columnconfigure(1, weight=2)

        # Δημιουργία των widgets για τη διαχείριση ραντεβού
        self.appointment_frame = ttk.LabelFrame(self.tab, text="Διαχείριση Ραντεβού")
        self.appointment_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.appointment_frame.grid_rowconfigure(0, weight=1)
        self.appointment_frame.grid_columnconfigure(0, weight=1)

        self.info_frame = ttk.Frame(self.appointment_frame)
        self.info_frame.pack(fill="x", expand=True)

        # Πεδία εισαγωγής
        self.phone_label = ttk.Label(self.info_frame, text="Τηλέφωνο     :")
        self.phone_label.grid(row=0, column=0)
        self.phone_entry = ttk.Entry(self.info_frame)
        self.phone_entry.grid(row=0, column=1, sticky="ew", padx=5, pady=5)

        self.date_label = ttk.Label(self.info_frame, text="Ημερομηνία   :")
        self.date_label.grid(row=1, column=0)
        self.date_entry = DateEntry(self.info_frame, date_pattern="dd/mm/yyyy")
        self.date_entry.grid(row=1, column=1, sticky="ew", padx=5, pady=5)

        self.time_label = ttk.Label(self.info_frame, text="Ώρα                :")
        self.time_label.grid(row=2, column=0)
        times = [
            f"{hour:02d}:{minute:02d}" for hour in range(8, 21) for minute in (0, 30)
        ]

        self.time_combo = ttk.Combobox(self.info_frame, values=times)
        self.time_combo.grid(row=2, column=1, sticky="ew", padx=5, pady=5)

        self.duration_label = ttk.Label(self.info_frame, text="Διάρκεια         :")
        self.duration_label.grid(row=3, column=0)
        self.duration_entry = ttk.Entry(self.info_frame)
        self.duration_entry.insert(
            0, "20"
        )  # Ορίζει την προεπιλεγμένη διάρκεια στα 20 λεπτά
        self.duration_entry.grid(row=3, column=1, sticky="ew", padx=5, pady=5)

        self.employee_label = ttk.Label(self.info_frame, text="Υπάλληλος    :")
        self.employee_label.grid(row=4, column=0)
        self.employee_combobox = ttk.Combobox(self.info_frame)
        self.employee_combobox.grid(row=4, column=1, sticky="ew", padx=5, pady=5)

        self.comments_label = ttk.Label(self.info_frame, text="Σχόλια            :")
        self.comments_label.grid(row=5, column=0)
        self.comments_text = tk.Text(self.info_frame, width=30, height=10)
        self.comments_text.grid(row=5, column=1, sticky="ew", padx=5, pady=5)

        # Κουμπιά επεξεργασίας
        self.buttons_frame = ttk.Frame(self.appointment_frame)
        self.buttons_frame.pack(fill="x", expand=True)

        self.add_button = ttk.Button(
            self.buttons_frame, text="Προσθήκη", command=self.add_appointment
        )
        self.add_button.grid(row=0, column=0, padx=5, pady=5)

        self.edit_button = ttk.Button(self.buttons_frame, text="Επεξεργασία")
        self.edit_button.grid(row=0, column=1, padx=5, pady=5)

        self.delete_button = ttk.Button(self.buttons_frame, text="Διαγραφή")
        self.delete_button.grid(row=0, column=2, padx=5, pady=5)

        self.delete_button = ttk.Button(self.buttons_frame, text="Εξαγωγή", command=lambda: export_all_appointments_to_xlsx(self.appointment_manager, self.client_manager, "exports"))
        self.delete_button.grid(row=0, column=3, padx=5, pady=5)

        # Δημιουργία των widgets για τη λίστα ραντεβού
        self.list_frame = ttk.LabelFrame(self.tab, text="Λίστα Ραντεβού")
        self.list_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        self.list_frame.grid_rowconfigure(0, weight=1)
        self.list_frame.grid_columnconfigure(0, weight=1)

        self.scrollbar = ttk.Scrollbar(self.list_frame)
        self.scrollbar.pack(side="right", fill="y")

        self.listbox = tk.Listbox(self.list_frame, yscrollcommand=self.scrollbar.set)
        self.listbox.pack(side="left", fill="both", expand=True)

        self.scrollbar.config(command=self.listbox.yview)

        # Πεδία αναζήτησης
        self.search_frame = ttk.Frame(self.list_frame)
        self.search_frame.pack(fill="x", expand=True)

        # Πεδίο αναζήτησης για ημερομηνία
        self.date_search_frame = ttk.Frame(self.search_frame)
        self.date_search_frame.pack(fill="x", expand=True)

        self.date_search_label = ttk.Label(
            self.date_search_frame, text="Αναζήτηση με ημερομηνία           :"
        )
        self.date_search_label.pack(side="left", padx=5, pady=5)

        self.date_search_entry = DateEntry(
            self.date_search_frame, date_pattern="dd/mm/yyyy"
        )
        self.date_search_entry.pack(side="left", fill="x", expand=True, padx=5, pady=5)

        self.date_search_button = ttk.Button(self.date_search_frame, text="Αναζήτηση")
        self.date_search_button.pack(side="left", padx=5, pady=5)

        # Πεδίο αναζήτησης για τον πελάτη
        self.client_search_frame = ttk.Frame(self.search_frame)
        self.client_search_frame.pack(fill="x", expand=True)

        self.client_search_label = ttk.Label(
            self.client_search_frame, text="Αναζήτηση με τηλέφωνο/Email  :"
        )
        self.client_search_label.pack(side="left", padx=5, pady=5)

        self.client_search_entry = ttk.Entry(self.client_search_frame)
        self.client_search_entry.pack(
            side="left", fill="x", expand=True, padx=5, pady=5
        )

        self.client_search_button = ttk.Button(
            self.client_search_frame, text="Αναζήτηση"
        )
        self.client_search_button.pack(side="left", padx=5, pady=5)

        self.populate_listbox()

    def clear_fields(self):
        self.comments_text.delete("1.0", "end")
        self.phone_entry.delete(0, "end")
        self.date_entry.delete(0, "end")
        self.time_combo.delete(0, "end")
        self.duration_entry.delete(0, "end")
        self.employee_combobox.delete(0, "end")

    def get_fields(self):
        return [
            self.comments_text.get("1.0", "end"),
            self.phone_entry.get(),
            self.date_entry.get(),
            self.time_combo.get(),
            self.duration_entry.get(),
            self.employee_combobox.get(),
        ]

    def populate_listbox(self, appointments=None):
        self.listbox.delete(0, "end")

        if not appointments:
            appointments = self.appointment_manager.get_all_appointments()
            print(appointments)

        for a in appointments:
            id, name, date, duration, client_id, employee_id = a
            self.listbox.insert(
                "end", f"{id} {name} {date} {duration} {client_id} {employee_id}"
            )

    def add_appointment(self):
        fields = self.get_fields()
        print(fields)
        emp_name = fields[5]
        phone = fields[1]
        client_id = self.client_manager.get_id_from_phone(phone)[0]
        employee_id = self.employee_manager.get_id_from_name(emp_name)
        print(fields[2])
        self.appointment_manager.add_appointment(
            fields[0].strip(),
            datetime.strptime(f"{fields[2]} {fields[3]}", "%d/%m/%Y %H:%M"),
            int(fields[4]),
            client_id,
            employee_id,
        )

        self.clear_fields()
        self.populate_listbox()
