from client_manager import ClientManager
import tkinter as tk
from tkinter import StringVar
from tkinter import ttk

DATABASE_FILE = "app.db"


class Customers:
    def __init__(self, tab):
        self.client_manager = ClientManager(DATABASE_FILE)
        self.curselection = 0
        self.search_terms = StringVar()
        self.search_terms.trace("w", lambda *args: self.search_client())
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

        self.add_button = ttk.Button(
            self.buttons_frame, text="Προσθήκη", command=self.add_client
        )
        self.add_button.grid(row=0, column=0, padx=5, pady=5)

        self.edit_button = ttk.Button(
            self.buttons_frame, text="Επεξεργασία", command=self.edit_client
        )
        self.edit_button.grid(row=0, column=1, padx=5, pady=5)

        self.update_button = ttk.Button(
            self.buttons_frame, text="Ανανέωση", command=self.update_client
        )
        self.update_button.grid(row=1, column=1, padx=5, pady=5)

        self.delete_button = ttk.Button(
            self.buttons_frame, text="Διαγραφή", command=self.delete_client
        )
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

        self.search_entry = ttk.Entry(self.search_frame, textvariable=self.search_terms)
        self.search_entry.pack(side="left", fill="x", expand=True, padx=5, pady=5)

        # self.search_button = ttk.Button(self.search_frame, text="Αναζήτηση")
        # self.search_button.pack(side="right", padx=5, pady=5)

        self.populate_listbox()

    # methods για τα κουμπια
    def get_client_id_from_listbox(self):
        values = self.listbox.curselection()
        index = values[0]
        self.curselection = int(self.listbox.get(index).split()[0])

    def clear_fields(self):
        self.name_entry.delete(0, "end")
        self.surname_entry.delete(0, "end")
        self.phone_entry.delete(0, "end")
        self.email_entry.delete(0, "end")

    def populate_listbox(self, clients=None):
        # Clear the current listbox content
        self.listbox.delete(0, "end")

        # Fetch clients from the database
        if not clients:
            clients = self.client_manager.get_all_clients()

        # Populate the listbox with client data
        for client in clients:
            client_id, first_name, last_name, phone, email = client
            self.listbox.insert(
                "end", f"{client_id} {first_name} {last_name} {phone} {email}"
            )

    def add_client(self):
        first_name = self.name_entry.get()
        last_name = self.surname_entry.get()
        phone = self.phone_entry.get()
        email = self.email_entry.get()
        success = self.client_manager.add_client(first_name, last_name, phone, email)
        if success:
            self.clear_fields()
        self.populate_listbox()

    def edit_client(self):
        self.get_client_id_from_listbox()
        client = self.client_manager.get_client(self.curselection)
        self.clear_fields()
        self.name_entry.insert(0, client[1])
        self.surname_entry.insert(0, client[2])
        self.phone_entry.insert(0, client[3])
        self.email_entry.insert(0, client[4])

    def update_client(self):
        first_name = self.name_entry.get()
        last_name = self.surname_entry.get()
        phone = self.phone_entry.get()
        email = self.email_entry.get()
        self.client_manager.update_client(
            self.curselection, first_name, last_name, phone, email
        )
        self.clear_fields()
        self.populate_listbox()

    def delete_client(self):
        self.get_client_id_from_listbox()
        self.client_manager.delete_client(self.curselection)
        self.clear_fields()
        self.populate_listbox()

    def search_client(self):
        search_term = self.search_terms.get()
        self.name_entry.insert(0, search_term)
        clients = self.client_manager.search_clients(search_term)
        self.clear_fields()
        self.populate_listbox(clients)
