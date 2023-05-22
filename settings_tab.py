import tkinter as tk
from tkinter import ttk
import webbrowser
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from employee_manager import EmployeeManager

DATABASE_FILE = "app.db"


class Settings:
    def __init__(self, tab):
        self.employee_manager = EmployeeManager(DATABASE_FILE)
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

        # Διάγραμμα απόδοσης υπαλλήλων
        self.fig = plt.Figure(figsize=(4, 4), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.ax.set_title("Διάγραμμα απόδοσης υπαλλήλων")
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.employee_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        # Κουμπιά επεξεργασίας
        self.buttons_frame = ttk.Frame(self.employee_frame)
        self.buttons_frame.pack(fill="x", expand=True)

        self.report_button = ttk.Button(
            self.buttons_frame, text="Έκθεση", command=self.open_report
        )
        self.report_button.grid(row=0, column=0)

        self.guide_button = ttk.Button(self.buttons_frame, text="Οδηγίες")
        self.guide_button.grid(row=0, column=1)

        self.update_button = ttk.Button(
            self.buttons_frame, text="Ενημέρωση Διαγράμματος", command=self.update_plot
        )
        self.update_button.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

        # Δημιουργία των widgets για τη λίστα υπαλλήλων
        self.list_frame = ttk.LabelFrame(self.tab, text="Λίστα Υπαλλήλων")
        self.list_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        self.list_frame.grid_rowconfigure(0, weight=1)
        self.list_frame.grid_columnconfigure(0, weight=1)

        # Λίστα υπαλλήλων
        self.employees_list = ttk.Treeview(
            self.list_frame, columns=("name", "surname"), show="headings"
        )
        self.employees_list.heading("name", text="Όνομα")
        self.employees_list.heading("surname", text="Επώνυμο")
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

        self.add_button = ttk.Button(
            self.buttons_frame, text="Προσθήκη", command=self.add_employee
        )
        self.add_button.grid(row=1, column=2, padx=5, pady=5)

        self.delete_button = ttk.Button(
            self.buttons_frame, text="Διαγραφή", command=self.delete_employee
        )
        self.delete_button.grid(row=1, column=3, padx=5, pady=5)

        # Σύνδεση κουμπιών με λειτουργίες
        self.add_button.config(command=self.add_employee)
        self.delete_button.config(command=self.delete_employee)

    def open_report(self):
        webbrowser.open("SchedulEasy.pdf")

    def add_employee(self):
        name = self.name_entry.get()
        surname = self.surname_entry.get()

        if name and surname:  # Αν τα πεδία δεν είναι κενά
            self.employees_list.insert(
                "", "end", values=(name, surname)
            )  # Προσθήκη στη λίστα
            self.name_entry.delete(0, "end")  # Καθαρισμός των πεδίων
            self.surname_entry.delete(0, "end")

    def delete_employee(self):
        selected_items = self.employees_list.selection()  # Λήψη επιλεγμένων στοιχείων
        for item in selected_items:
            self.employees_list.delete(item)  # Διαγραφή από τη λίστα

    def update_plot(self):
        # Εδώ πρέπει να ενημερώσετε τα δεδομένα του διαγράμματος σύμφωνα με τη βάση δεδομένων
        # Αυτό είναι ένα παράδειγμα:
        self.ax.cla()  # clear the plot
        self.ax.set_title("Διάγραμμα απόδοσης υπαλλήλων")
        data = [
            20,
            15,
            30,
            25,
            10,
            34,
            25,
            40,
            22,
            80,
        ]  # Αυτά είναι δεδομένα επίδοσης των υπαλλήλων για παράδειγμα
        self.ax.barh(
            [
                "Υπάλληλος 1",
                "Υπάλληλος 2",
                "Υπάλληλος 3",
                "Υπάλληλος 4",
                "Υπάλληλος 5",
                "Υπάλληλος 6",
                "Υπάλληλος 7",
                "Υπάλληλος 8",
                "Υπάλληλο 9",
                "Υπάλληλος 10",
            ],
            data,
        )
        self.canvas.draw()
