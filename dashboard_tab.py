import tkinter as tk
from tkinter import StringVar, ttk

from PIL import Image, ImageTk
from tkcalendar import DateEntry

from appointment_manager import AppointmentManager
from client_manager import ClientManager
from employee_manager import EmployeeManager

from utils import export_all_appointments_to_xlsx
from utils import send_reminders_to_clients_at_date


DATABASE_FILE = "app.db"


class Dashboard:
    def __init__(self, tab):
        self.tab = tab
        self.search_terms = StringVar()
        self.client_manager = ClientManager(DATABASE_FILE)
        self.appointment_manager = AppointmentManager(DATABASE_FILE)
        self.employee_manager = EmployeeManager(DATABASE_FILE)
        self.tab.grid_rowconfigure(0, weight=1)
        self.tab.grid_columnconfigure(0, weight=2)
        self.tab.grid_columnconfigure(1, weight=1)

        # Φορτώνει την εικόνα
        image_path = "logo.png"
        image = Image.open(image_path)
        photo = ImageTk.PhotoImage(image)

        # Δημιουργία των widgets για τη λίστα ραντεβού
        self.appointment_frame = ttk.LabelFrame(self.tab, text="Ραντεβού της Ημέρας")
        self.appointment_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.appointment_frame.grid_rowconfigure(0, weight=1)
        self.appointment_frame.grid_columnconfigure(0, weight=1)

        self.scrollbar = ttk.Scrollbar(self.appointment_frame)
        self.scrollbar.pack(side="right", fill="y")

        self.listbox = tk.Listbox(
            self.appointment_frame, yscrollcommand=self.scrollbar.set
        )
        self.listbox.pack(side="left", fill="both", expand=True)

        self.scrollbar.config(command=self.listbox.yview)

        # Κουμπιά διαχείρισης
        self.buttons_frame = ttk.Frame(self.appointment_frame)
        self.buttons_frame.pack(fill="x", expand=True)

        self.date_label = ttk.Label(self.buttons_frame, text="Ημερομηνία   :")
        self.date_label.grid(row=0, column=2, padx=5, pady=5)

        self.date_entry = DateEntry(self.buttons_frame, date_pattern="dd/mm/yyyy")
        self.date_entry.bind(
            "<<DateEntrySelected>>", lambda event: self.search_appointments()
        )
        self.date_entry.grid(row=0, column=3, padx=5, pady=5)

        self.remind_button = ttk.Button(self.buttons_frame, text="Αποστολή Υπενθύμισης", command=self.remind_clients)
        self.remind_button.grid(row=1, column=2, padx=5, pady=5)

        self.print_button = ttk.Button(
            self.buttons_frame,
            text="Εκτύπωση Ραντεβού",
            command=self.print_appointments,
        )
        self.print_button.grid(row=1, column=3, padx=5, pady=5)

        # Δημιουργία των widgets για την ομάδα προγραμματιστών
        self.dev_frame = ttk.LabelFrame(self.tab, text="SchedulEase: Version 0.1")
        self.dev_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        self.dev_frame.grid_rowconfigure(0, weight=1)
        self.dev_frame.grid_columnconfigure(0, weight=1)

        # Φορτώνει και ορίζει την εικόνα φόντου
        background_image = Image.open("background.png")
        background_image = ImageTk.PhotoImage(background_image)
        background_label = tk.Label(self.dev_frame, image=background_image)
        # Keep a reference to the image to prevent garbage collection
        background_label.image = background_image
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        developer_info = (
            "ΠΛΗΠΡΟ - ΗΛΕ45\n\nΟΜΑΔΑ\nΓαλατσάνος Δημήτριος\nΛόλας Ιωάννης\nΜορτόπουλος Αγησίλαος"
            "\nΧαλίδου Μαρία\nΚουτσουρίδης Ανέστης"
        )
        self.developer_label = ttk.Label(self.dev_frame, text=developer_info)
        self.developer_label.grid(row=0, column=0, padx=5, pady=5)

        # Προσθέστε την εικόνα σε ένα Label
        self.logo_label = ttk.Label(self.dev_frame, image=photo)
        self.logo_label.image = photo  # keep a reference!
        self.logo_label.grid(row=1, column=1, padx=5, pady=5)

        self.search_appointments()

    def search_appointments(self):
        self.listbox.delete(0, "end")
        date = self.date_entry.get()
        parts = date.split("/")
        date = f"{parts[2]}-{parts[1]}-{parts[0]}"
        appointments = self.appointment_manager.get_appointments_on_date(date)

        for a in appointments:
            id, name, date, duration, client_id, employee_id = a
            client = (
                self.client_manager.get_client(client_id)[1]
                + " "
                + self.client_manager.get_client(client_id)[2]
            )
            employee = self.employee_manager.get_employee(employee_id)[1]
            self.listbox.insert(
                "end",
                f"{id} {client} at: {date} for: {duration}mins {name} with: {employee}",
            )

    def print_appointments(self):
        date = self.date_entry.get()
        parts = date.split("/")
        date = f"{parts[2]}-{parts[1]}-{parts[0]}"
        export_all_appointments_to_xlsx(
            self.appointment_manager,
            self.client_manager,
            "exports",
            date,
        )

    def remind_clients(self):
        date = self.date_entry.get()
        parts = date.split("/")
        date = f"{parts[2]}-{parts[1]}-{parts[0]}"
        send_reminders_to_clients_at_date(self.appointment_manager, self.client_manager, date)
