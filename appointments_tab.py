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

        class UpdatingCombobox(ttk.Combobox):
            def __init__(self, *args, update_func=None, **kwargs):
                super().__init__(*args, **kwargs)
                self.update_func = update_func
                self.bind('<Button-1>', self.update_values)

            def update_values(self, event=None):
                if self.update_func:
                    self['values'] = self.update_func()

        self.appointment_manager = AppointmentManager(DATABASE_FILE)
        self.employee_manager = EmployeeManager(DATABASE_FILE)
        self.client_manager = ClientManager(DATABASE_FILE)
        self.curselection = 0
        self.search_terms = StringVar()
        self.search_terms.trace("w", lambda *args: self.search_appointments())
        self.tab = tab
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
        times = [f"{hour:02d}:{minute:02d}" for hour in range(8, 21) for minute in (0, 30)]

        self.time_combo = ttk.Combobox(self.info_frame, values=times)
        self.time_combo.grid(row=2, column=1, sticky="ew", padx=5, pady=5)

        self.duration_label = ttk.Label(self.info_frame, text="Διάρκεια         :")
        self.duration_label.grid(row=3, column=0)
        self.duration_entry = ttk.Entry(self.info_frame)
        self.duration_entry.insert(0, "20")  
        
        # Ορίζει την προεπιλεγμένη διάρκεια στα 20 λεπτά
        self.duration_entry.grid(row=3, column=1, sticky="ew", padx=5, pady=5)

        self.employee_label = ttk.Label(self.info_frame, text="Υπάλληλος    :")
        self.employee_label.grid(row=4, column=0)
        self.employee_combobox = ttk.Combobox(self.info_frame)
        self.employee_combobox = UpdatingCombobox(self.info_frame, update_func=self.update_employee_values)
        self.employee_combobox.grid(row=4, column=1, sticky="ew", padx=5, pady=5)

        self.comments_label = ttk.Label(self.info_frame, text="Σχόλια            :")
        self.comments_label.grid(row=5, column=0)
        self.comments_text = tk.Text(self.info_frame, width=30, height=10)
        self.comments_text.grid(row=5, column=1, sticky="ew", padx=5, pady=5)

        # Κουμπιά επεξεργασίας
        self.buttons_frame = ttk.Frame(self.appointment_frame)
        self.buttons_frame.pack(fill="x", expand=True)

        self.add_button = ttk.Button(self.buttons_frame, text="Προσθήκη", command=self.add_appointment)
        self.add_button.grid(row=0, column=0, padx=5, pady=5)

        self.edit_button = ttk.Button(self.buttons_frame, text="Επεξεργασία", command=self.edit_appointment)
        self.edit_button.grid(row=0, column=1, padx=5, pady=5)

        self.update_button = ttk.Button(self.buttons_frame, text="Ανανέωση", command=self.update_appointment)
        self.update_button.grid(row=1, column=1, padx=5, pady=5)

        self.delete_button = ttk.Button(self.buttons_frame, text="Διαγραφή", command=self.delete_appointment)
        self.delete_button.grid(row=0, column=2, padx=5, pady=5)

        self.delete_button = ttk.Button(self.buttons_frame, text="Εξαγωγή", command=lambda: export_all_appointments_to_xlsx(self.appointment_manager, self.client_manager, "exports"),)
        self.delete_button.grid(row=0, column=3, padx=5, pady=5)

        # Δημιουργία των widgets για τη λίστα ραντεβού
        self.list_frame = ttk.LabelFrame(self.tab, text="Λίστα Ραντεβού")
        self.list_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        self.list_frame.grid_rowconfigure(0, weight=1)
        self.list_frame.grid_columnconfigure(0, weight=1)

        self.tree = ttk.Treeview(
            self.list_frame,
            columns=("ID", "Πελάτης", "Ημέρα και Ώρα", "Διάρκεια", "Σχόλια", "Υπάλληλος"),
            show='headings'
        )

        self.tree.pack(side="left", fill="both", expand=True)

        self.tree.column("ID", width=50)
        self.tree.heading("ID", text="ID")
        self.tree.column("Πελάτης", width=100)
        self.tree.heading("Πελάτης", text="Πελάτης")
        self.tree.column("Ημέρα και Ώρα", width=100)
        self.tree.heading("Ημέρα και Ώρα", text="Ημέρα και Ώρα")
        self.tree.column("Διάρκεια", width=100)
        self.tree.heading("Διάρκεια", text="Διάρκεια")
        self.tree.column("Σχόλια", width=150)
        self.tree.heading("Σχόλια", text="Σχόλια")
        self.tree.column("Υπάλληλος", width=150)
        self.tree.heading("Υπάλληλος", text="Υπάλληλος")

        self.scrollbar = ttk.Scrollbar(self.list_frame, command=self.tree.yview)
        self.scrollbar.pack(side="right", fill="y")
        self.tree.config(yscrollcommand=self.scrollbar.set)

        # Πεδίο αναζήτησης
        self.search_frame = ttk.Frame(self.list_frame)
        self.search_frame.pack(fill="x", expand=True)

        self.search_entry = ttk.Entry(self.search_frame, textvariable=self.search_terms)
        self.search_entry.pack(side="right", fill="x", expand=True, padx=5, pady=5)

        self.search_label = ttk.Label(self.search_frame, text="Αναζήτηση  :")
        self.search_label.pack(side="left", fill="x", expand=True, padx=5, pady=5)

        self.populate_treeview()

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

    def populate_treeview(self, appointments=None, show_empty=False):
        for i in self.tree.get_children():
            self.tree.delete(i)

        if show_empty:
            return

        if not appointments:
            appointments = self.appointment_manager.get_all_appointments()

        for a in appointments:
            id, name, date, duration, client_id, employee_id = a
            client = (
                self.client_manager.get_client(client_id)[1]
                + " "
                + self.client_manager.get_client(client_id)[2]
            )
            employee = self.employee_manager.get_employee(employee_id)[1]
            self.tree.insert("", "end", values=(id, client, date, duration, name, employee))


    def add_appointment(self):
        fields = self.get_fields()
        emp_name = fields[5]
        phone = fields[1]
        client_id = self.client_manager.get_id_from_phone(phone)[0]
        employee_id = self.employee_manager.get_id_from_name(emp_name)[0]
        print(fields[2])
        self.appointment_manager.add_appointment(
            fields[0].strip(),
            datetime.strptime(f"{fields[2]} {fields[3]}", "%d/%m/%Y %H:%M"),
            int(fields[4]),
            client_id,
            employee_id,
        )

        self.clear_fields()
        self.populate_treeview()

    def get_appointment_id_from_treeview(self):
        cur_item = self.tree.focus()
        item_values = self.tree.item(cur_item)['values']
        self.curselection = int(item_values[0])

    def edit_appointment(self):
        self.get_appointment_id_from_treeview()
        apt = self.appointment_manager.get_appointment(self.curselection)
        self.clear_fields()

        client_id = apt[4]
        phone = self.client_manager.get_client(client_id)[3]

        self.phone_entry.insert(0, phone)
        self.duration_entry.insert(0, apt[3])

    def update_appointment(self):
        fields = self.get_fields()
        emp_name = fields[5]
        phone = fields[1]
        client_id = self.client_manager.get_id_from_phone(phone)[0]
        employee_id = self.employee_manager.get_id_from_name(emp_name)[0]
        print(fields[2])
        self.appointment_manager.update_appointment(
            self.curselection,
            fields[0].strip(),
            datetime.strptime(f"{fields[2]} {fields[3]}", "%d/%m/%Y %H:%M"),
            int(fields[4]),
            client_id,
            employee_id,
        )

        self.clear_fields()
        self.populate_treeview()

    def delete_appointment(self):
        self.get_appointment_id_from_treeview()
        self.appointment_manager.delete_appointment(self.curselection)
        self.populate_treeview()


    def search_appointments(self):
        search_term = self.search_terms.get().lower()
        appointments = self.appointment_manager.get_all_appointments()
        filtered = []
        for a in appointments:
            id, name, date, duration, client_id, employee_id = a
            client = (
                self.client_manager.get_client(client_id)[1]
                + " "
                + self.client_manager.get_client(client_id)[2]
            )
            employee = self.employee_manager.get_employee(employee_id)[1]
            appointment_string = f"{id} {client} at: {date} for: {duration}mins {name} with: {employee}"
            if search_term in appointment_string.lower():
                filtered.append(a)
        
        if not filtered:
            self.populate_treeview(appointments, True)
        else:
            self.populate_treeview(filtered)

    def update_employee_values(self):
        return [emp[1] for emp in self.employee_manager.get_all_employees()]