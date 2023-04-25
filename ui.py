import tkinter as tk
from tkinter import Tk
from tkinter import ttk
from tkinter import Label
from tkinter import messagebox
from tkinter import Button
from tkinter import Menu
from tkinter import Frame
from tkinter import Entry
from tkinter import StringVar
from ttkthemes import ThemedTk


class Ui:
    def __init__(self, client_manager):
        self.client_manager = client_manager

        # ui init
        self.root = ThemedTk(theme="arc")
        # Set up the main window
        self.root.title("Appointment Management")
        self.root.geometry("1800x1000")
        # self.root.center_window()

        # Apply styles for the tabs
        self.root.style = ttk.Style()
        self.root.style.configure(
            "TNotebook.Tab",
            background="#5c9fd7",
            foreground="grey",
            padding=[16, 8],
            font=("Arial", 12, "bold"),
        )
        self.root.style.map("TNotebook.Tab", background=[("selected", "#3c7adb")])

        # Set up the notebook (tabs)
        self.notebook = ttk.Notebook(self.root)
        # check what is happening here
        self.notebook.pack(expand=True, fill=tk.BOTH)

        # Create the Customer Management tab
        self.customer_tab = ttk.Frame(self.root)
        self.notebook.add(self.customer_tab, text="Customer Management")

        # Create the Appointment Management tab
        self.appointment_tab = ttk.Frame(self.root)
        self.notebook.add(self.appointment_tab, text="Appointment Management")

        # Set up the content for each tab
        self.create_customer_tab_content()
        # self.create_appointment_tab_content()

        self.root.mainloop()

    def populate_customers_listbox(self):
        # Clear the current listbox content
        for item in self.customers_listbox.get_children():
            self.customers_listbox.delete(item)

        # Fetch customers from the database
        customers = self.client_manager.get_all_clients()
        print(customers)

        # Populate the listbox with customer data
        for customer in customers:
            customer_id, first_name, last_name, phone, email = customer
            self.customers_listbox.insert(
                "", tk.END, values=(first_name, last_name, phone, email)
            )

    def add_client(self):
        first_name = self.first_name_entry.get()
        last_name = self.last_name_entry.get()
        phone = self.phone_entry.get()
        email = self.email_entry.get()
        self.client_manager.add_client(first_name, last_name, phone, email)
        self.first_name_entry.delete(0, tk.END)
        self.last_name_entry.delete(0, tk.END)
        self.phone_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.populate_customers_listbox()

    def create_customer_tab_content(self):
        # First Name
        ttk.Label(self.customer_tab, text="First Name:").grid(
            row=0, column=0, padx=10, pady=10, sticky=tk.W
        )
        self.first_name_entry = ttk.Entry(self.customer_tab)
        self.first_name_entry.grid(row=0, column=1, padx=10, pady=10, sticky=tk.W)

        # Last Name
        ttk.Label(self.customer_tab, text="Last Name:").grid(
            row=1, column=0, padx=10, pady=10, sticky=tk.W
        )
        self.last_name_entry = ttk.Entry(self.customer_tab)
        self.last_name_entry.grid(row=1, column=1, padx=10, pady=10, sticky=tk.W)

        # Phone
        ttk.Label(self.customer_tab, text="Phone:").grid(
            row=2, column=0, padx=10, pady=10, sticky=tk.W
        )
        self.phone_entry = ttk.Entry(self.customer_tab)
        self.phone_entry.grid(row=2, column=1, padx=10, pady=10, sticky=tk.W)

        # Email
        ttk.Label(self.customer_tab, text="Email:").grid(
            row=3, column=0, padx=10, pady=10, sticky=tk.W
        )
        self.email_entry = ttk.Entry(self.customer_tab)
        self.email_entry.grid(row=3, column=1, padx=10, pady=10, sticky=tk.W)

        self.search_customer_var = tk.StringVar()
        self.search_customer_entry = ttk.Entry(
            self.customer_tab, textvariable=self.search_customer_var
        )
        self.search_customer_entry.grid(row=6, column=0, pady=5)

        # Buttons
        self.add_customer_button = ttk.Button(
            self.customer_tab,
            text="Add Customer",
            command=self.add_client,
        )
        self.add_customer_button.grid(row=4, column=0, padx=10, pady=10, sticky=tk.W)

        self.update_customer_button = ttk.Button(
            self.customer_tab,
            text="Update Customer",
            command=self.client_manager.update_client,
        )
        self.update_customer_button.grid(row=4, column=1, padx=10, pady=10, sticky=tk.W)

        self.delete_customer_button = ttk.Button(
            self.customer_tab,
            text="Delete Customer",
            command=self.client_manager.delete_client,
        )
        self.delete_customer_button.grid(row=4, column=2, padx=10, pady=10, sticky=tk.W)

        self.search_customer_button = ttk.Button(
            self.customer_tab,
            text="Search Customer",
            command=self.client_manager.search_client,
        )
        self.search_customer_button.grid(row=6, column=1, padx=10, pady=10, sticky=tk.W)

        # Listbox to display customers
        self.customers_listbox = ttk.Treeview(
            self.customer_tab,
            columns=("First Name", "Last Name", "Phone", "Email"),
            show="headings",
        )
        self.customers_listbox.heading("First Name", text="First Name")
        self.customers_listbox.heading("Last Name", text="Last Name")
        self.customers_listbox.heading("Phone", text="Phone")
        self.customers_listbox.heading("Email", text="Email")
        self.customers_listbox.grid(
            row=5, column=0, columnspan=3, padx=10, pady=10, sticky=tk.W + tk.E
        )

        # Scrollbar for the listbox
        self.customers_listbox_scrollbar = ttk.Scrollbar(
            self.customer_tab, orient="vertical", command=self.customers_listbox.yview
        )
        self.customers_listbox_scrollbar.grid(row=5, column=3, sticky=tk.N + tk.S)
        self.customers_listbox.configure(
            yscrollcommand=self.customers_listbox_scrollbar.set
        )

        # Populate the listbox with existing customers (from the database)
        self.populate_customers_listbox()
