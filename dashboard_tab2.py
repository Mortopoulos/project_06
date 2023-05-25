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

        self.tree = ttk.Treeview(self.appointment_frame, selectmode="browse")
        self.tree.pack(side="left", fill="both", expand=True)

        vsb = ttk.Scrollbar(self.appointment_frame, orient="vertical", command=self.tree.yview)
        vsb.pack(side='left', fill='y')

        self.tree.configure(yscrollcommand=vsb.set)

        self.tree["columns"] = ("id", "Πελάτης", "Ημέρα και Ώρα", "Διάρκεια", "Σχόλια", "Υπάλληλος")
        self.tree.column("#0", width=0, stretch=False)
        self.tree.column("id", width=0, stretch=False)  
        self.tree.column("Πελάτης", width=10, stretch=True)  
        self.tree.column("Ημέρα και Ώρα", width=10, stretch=True) 
        self.tree.column("Διάρκεια", width=10, stretch=True) 
        self.tree.column("Σχόλια", width=10, stretch=True) 
        self.tree.column("Υπάλληλος", width=10, stretch=True)

        for col in self.tree["columns"][1:]:
            self.tree.heading(col, text=col)

        # Κουμπιά διαχείρισης
        
        self.buttons_frame = ttk.Frame(self.tab)
        self.buttons_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=10)  # Place the buttons below the Treeview

        self.date_label = ttk.Label(self.buttons_frame, text="Ημερομηνία   :")
        self.date_label.grid(row=0, column=2, padx=5, pady=5)

        self.date_entry = DateEntry(self.buttons_frame, date_pattern="dd/mm/yyyy")
        self.date_entry.bind("<<DateEntrySelected>>", lambda event: self.search_appointments())
        self.date_entry.grid(row=0, column=3, padx=5, pady=5)

        self.remind_button = ttk.Button(self.buttons_frame, text="Αποστολή Υπενθύμισης", command=self.remind_clients)
        self.remind_button.grid(row=1, column=2, padx=5, pady=5)

        self.print_button = ttk.Button(self.buttons_frame, text="Εκτύπωση Ραντεβού", command=self.print_appointments,)
        self.print_button.grid(row=1, column=3, padx=5, pady=5)

        # Don't forget to adjust row weights after adding the new row
        self.tab.grid_rowconfigure(0, weight=1)  # for treeview
        self.tab.grid_rowconfigure(1, weight=0)  # for buttons_frame
        self.tab.grid_columnconfigure(0, weight=1)  # Maintain a small weight for column 0
        self.tab.grid_columnconfigure(1, weight=4)

        # Adjust the weight of the columns and rows in the main grid
        self.tab.grid_rowconfigure(0, weight=1)
        self.tab.grid_columnconfigure(0, weight=1)  # Maintain a small weight for column 0
        self.tab.grid_columnconfigure(1, weight=4)

        # Δημιουργία των widgets για την ομάδα προγραμματιστών
        self.dev_frame = ttk.LabelFrame(self.tab, text="SchedulEase: Version 1.0")
        self.dev_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        self.dev_frame.grid_rowconfigure(0, weight=1)
        self.dev_frame.grid_columnconfigure(0, weight=2)

        # Φορτώνει και ορίζει την εικόνα φόντου
        background_image = Image.open("background.png")
        background_image = ImageTk.PhotoImage(background_image)
        background_label = tk.Label(self.dev_frame, image=background_image)
       
        background_label.image = background_image
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        developer_info = (
            "ΠΛΗΠΡΟ - ΗΛΕ45\n\nΟΜΑΔΑ\nΓαλατσάνος Δημήτριος\nΛόλας Ιωάννης\nΜορτόπουλος Αγησίλαος"
            "\nΧαλίδου Μαρία"
        )
        self.developer_label = ttk.Label(self.dev_frame, text=developer_info)
        self.developer_label.grid(row=0, column=0, padx=5, pady=5)

        # Προσθέστε την εικόνα σε ένα Label
        self.logo_label = ttk.Label(self.dev_frame, image=photo)
        self.logo_label.image = photo  # keep a reference!
        self.logo_label.grid(row=1, column=1, padx=5, pady=5)

        self.search_appointments()

    def search_appointments(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
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
            self.tree.insert("", "end", values=(id, client, date, duration, name, employee))

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
