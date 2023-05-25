import tkinter as tk
from tkinter import ttk
import webbrowser
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from employee_manager import EmployeeManager
from appointment_manager import AppointmentManager

from utils import get_stats_in_date_range

DATABASE_FILE = "app.db"


class Settings:
    def __init__(self, tab):
        self.employee_manager = EmployeeManager(DATABASE_FILE)
        self.appointment_manager = AppointmentManager(DATABASE_FILE)
        self.tab = tab
        self.tab.grid_rowconfigure(0, weight=1)
        self.tab.grid_columnconfigure(0, weight=1)

        # Δημιουργία των widgets για τη διαχείριση υπαλλήλων
        self.employee_frame = ttk.LabelFrame(self.tab, text="Διαχείριση Εφαρμογής")
        self.employee_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.employee_frame.grid_rowconfigure(0, weight=1)
        self.employee_frame.grid_columnconfigure(0, weight=1)

        self.info_frame = ttk.Frame(self.employee_frame)
        self.info_frame.pack(fill="x", expand=True)

        # Κουμπιά επεξεργασίας
        self.buttons_frame = ttk.Frame(self.employee_frame)
        self.buttons_frame.pack(fill="x", expand=True)

        self.report_button = ttk.Button(self.buttons_frame, text="Έκθεση", command=self.open_report)
        self.report_button.grid(row=0, column=0)

        self.guide_button = ttk.Button(self.buttons_frame, text="Οδηγίες")
        self.guide_button.grid(row=0, column=1)


        # Δημιουργία των widgets για τη λίστα υπαλλήλων
        self.list_frame = ttk.LabelFrame(self.tab, text="Λίστα Υπαλλήλων")
        self.list_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        self.list_frame.grid_rowconfigure(0, weight=1)
        self.list_frame.grid_columnconfigure(0, weight=1)

        # Λίστα υπαλλήλων
        self.employees_list = ttk.Treeview(
            self.list_frame, columns=("name", "email"), show="headings"
        )
        self.employees_list.heading("name", text="Όνοματεπώνυμο")
        self.employees_list.heading("email", text="Email")
        self.employees_list.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        # Δημιουργία των widgets για την προσθήκη και διαγραφή υπαλλήλων
        self.buttons_frame = ttk.Frame(self.list_frame)
        self.buttons_frame.grid(row=1, column=0, sticky="ew", padx=5, pady=5)

        self.name_label = ttk.Label(self.buttons_frame, text="Όνομα        :")
        self.name_label.grid(row=0, column=0)

        self.name_entry = ttk.Entry(self.buttons_frame)
        self.name_entry.grid(row=0, column=1, sticky="ew", padx=5, pady=5)

        self.surname_label = ttk.Label(self.buttons_frame, text="Επώνυμο    :")
        self.surname_label.grid(row=1, column=0)

        self.surname_entry = ttk.Entry(self.buttons_frame)
        self.surname_entry.grid(row=1, column=1, sticky="ew", padx=5, pady=5)

        self.email_label = ttk.Label(self.buttons_frame, text="Email            :")
        self.email_label.grid(row=2, column=0)

        self.email_entry = ttk.Entry(self.buttons_frame)
        self.email_entry.grid(row=2, column=1, sticky="ew", padx=5, pady=5)

        self.passcode_label = ttk.Label(self.buttons_frame, text="Pass              :")
        self.passcode_label.grid(row=3, column=0)

        self.passcode_entry = ttk.Entry(self.buttons_frame)
        self.passcode_entry.grid(row=3, column=1, sticky="ew", padx=5, pady=5)

        self.add_button = ttk.Button(self.buttons_frame, text="Προσθήκη", command=self.add_employee)
        self.add_button.grid(row=3, column=2, padx=5, pady=5)

        self.delete_button = ttk.Button(self.buttons_frame, text="Διαγραφή", command=self.delete_employee)
        self.delete_button.grid(row=3, column=3, padx=5, pady=5)

        # Σύνδεση κουμπιών με λειτουργίες
        self.add_button.config(command=self.add_employee)
        self.delete_button.config(command=self.delete_employee)

        self.populate_listbox()

    def open_report(self):
        webbrowser.open("SchedulEasy.pdf")

    def clear_employee_list(self):
        for item in self.employees_list.get_children():
            self.employees_list.delete(item)

    def populate_listbox(self, employees=None):
        # Clear the current listbox content
        self.clear_employee_list()

        # Fetch clients from the database
        if not employees:
            employees = self.employee_manager.get_all_employees()

        # Populate the listbox with client data
        for emp in employees:
            emp_id, name, email, passcode = emp
            self.employees_list.insert("", "end", values=(name, email))  
            
    # Προσθήκη στη λίστα
    def add_employee(self):
        name = self.name_entry.get()
        surname = self.surname_entry.get()
        email = self.email_entry.get()
        passcode = self.passcode_entry.get()

        fullname = name + " " + surname

        if fullname and email and passcode:  
            print(fullname, email, passcode)
            self.employee_manager.add_employee(fullname, email, passcode)

        self.name_entry.delete(0, "end")  
        self.surname_entry.delete(0, "end")
        self.email_entry.delete(0, "end")
        self.passcode_entry.delete(0, "end")

        self.populate_listbox()

    def delete_employee(self):
        selected_items = self.employees_list.selection() 
        if selected_items: 
            for selected_item in selected_items:
                item = self.employees_list.item(selected_item)  
                name, email = item['values']  
                self.employee_manager.delete_employee(email)  
            self.tab.after(100, self.populate_listbox)
