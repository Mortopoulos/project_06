from client_manager import ClientManager
import tkinter as tk
from tkinter import ttk

DATABASE_FILE = "app.db"


class Customers:
    def __init__(self, tab):
        self.client_manager = ClientManager(DATABASE_FILE)
        self.tab = tab
        self.tab.grid_rowconfigure(0, weight=1)
        self.tab.grid_columnconfigure(0, weight=1)
        self.tab.grid_columnconfigure(1, weight=2)

        # Δημιουργία των widgets για τη διαχείριση πελατών
        self.customer_frame = ttk.LabelFrame(self.tab, text="Διαχείριση Πελατών")
        self.customer_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.customer_frame.grid_rowconfigure(0, weight=1)
        self.customer_frame.grid_columnconfigure(0, weight=1)

        self.info_frame = ttk.Frame(self.customer_frame)
        self.info_frame.pack(fill="x", expand=True)

        # Πεδία εισαγωγής
        self.name_label = ttk.Label(self.info_frame, text="Όνομα       :")
        self.name_label.grid(row=0, column=0)
        self.name_entry = ttk.Entry(self.info_frame)
        self.name_entry.grid(row=0, column=1, sticky="ew", padx=5, pady=5)

        self.surname_label = ttk.Label(self.info_frame, text="Επώνυμο  :")
        self.surname_label.grid(row=1, column=0)
        self.surname_entry = ttk.Entry(self.info_frame)
        self.surname_entry.grid(row=1, column=1, sticky="ew", padx=5, pady=5)

        self.phone_label = ttk.Label(self.info_frame, text="Τηλέφωνο :")
        self.phone_label.grid(row=2, column=0)
        self.phone_entry = ttk.Entry(self.info_frame)
        self.phone_entry.grid(row=2, column=1, sticky="ew", padx=5, pady=5)

        self.email_label = ttk.Label(self.info_frame, text="Email          :")
        self.email_label.grid(row=3, column=0)
        self.email_entry = ttk.Entry(self.info_frame)
        self.email_entry.grid(row=3, column=1, sticky="ew", padx=5, pady=5)

        # Κουμπιά επεξεργασίας
        self.buttons_frame = ttk.Frame(self.customer_frame)
        self.buttons_frame.pack(fill="x", expand=True)

        self.add_button = ttk.Button(self.buttons_frame, text="Προσθήκη")
        self.add_button.grid(row=0, column=0, padx=5, pady=5)

        self.edit_button = ttk.Button(self.buttons_frame, text="Επεξεργασία")
        self.edit_button.grid(row=0, column=1, padx=5, pady=5)

        self.delete_button = ttk.Button(self.buttons_frame, text="Διαγραφή")
        self.delete_button.grid(row=0, column=2, padx=5, pady=5)

        self.delete_button = ttk.Button(self.buttons_frame, text="Εξαγωγή")
        self.delete_button.grid(row=0, column=3, padx=5, pady=5)

        # Δημιουργία των widgets για τη λίστα πελατών
        self.list_frame = ttk.LabelFrame(self.tab, text="Λίστα Πελατών")
        self.list_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        self.list_frame.grid_rowconfigure(0, weight=1)
        self.list_frame.grid_columnconfigure(0, weight=1)

        self.scrollbar = ttk.Scrollbar(self.list_frame)
        self.scrollbar.pack(side="right", fill="y")

        self.listbox = tk.Listbox(self.list_frame, yscrollcommand=self.scrollbar.set)
        self.listbox.pack(side="left", fill="both", expand=True)

        self.scrollbar.config(command=self.listbox.yview)

        # Πεδίο αναζήτησης
        self.search_frame = ttk.Frame(self.list_frame)
        self.search_frame.pack(fill="x", expand=True)

        self.search_entry = ttk.Entry(self.search_frame)
        self.search_entry.pack(side="left", fill="x", expand=True, padx=5, pady=5)

        self.search_button = ttk.Button(self.search_frame, text="Αναζήτηση")
        self.search_button.pack(side="right", padx=5, pady=5)
