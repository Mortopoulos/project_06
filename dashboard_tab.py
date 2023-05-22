import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
from PIL import Image, ImageTk


class Dashboard:
    def __init__(self, tab):
        self.tab = tab
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
        self.date_entry.grid(row=0, column=3, padx=5, pady=5)

        self.remind_button = ttk.Button(self.buttons_frame, text="Αποστολή Υπενθύμισης")
        self.remind_button.grid(row=1, column=2, padx=5, pady=5)

        self.print_button = ttk.Button(self.buttons_frame, text="Εκτύπωση Ραντεβού")
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
        background_label.image = background_image  # Keep a reference to the image to prevent garbage collection
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
