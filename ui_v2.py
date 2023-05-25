import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk

from dashboard_tab import Dashboard
from customers_tab import Customers
from appointments_tab import Appointments
from settings_tab import Settings


class MainApplication:
    def __init__(self):
        self.root = ThemedTk(theme="Adapta")
        self.root.title("SchedulEasy")
        #self.root.iconbitmap('icon.ico')

        # Το παράθυρο θα καταλαμβάνει το 80% της οθόνης
        self.center_window(0.75, 0.75)

        # Ρυθμίζει το style των tabs
        style = ttk.Style()
        style.configure("TNotebook.Tab", font=("Helvetica", "12"), padding=[12, 6])

        # Δημιουργία tabs
        self.tab_parent = ttk.Notebook(self.root)

        self.dashboard_tab = ttk.Frame(self.tab_parent)
        self.customers_tab = ttk.Frame(self.tab_parent)
        self.appointments_tab = ttk.Frame(self.tab_parent)
        self.settings_tab = ttk.Frame(self.tab_parent)

        self.tab_parent.add(self.dashboard_tab, text="Πίνακας Ελέγχου")
        self.tab_parent.add(self.customers_tab, text="Πελάτες")
        self.tab_parent.add(self.appointments_tab, text="Ραντεβού")
        self.tab_parent.add(self.settings_tab, text="Ρυθμίσεις")

        self.tab_parent.pack(expand=1, fill="both")

        self.dashboard = Dashboard(self.dashboard_tab)
        self.customers = Customers(self.customers_tab)
        self.appointments = Appointments(self.appointments_tab)
        self.settings = Settings(self.settings_tab)
        self.root.mainloop()

    # Καθορίζει το μέγεθος του παραθύρου σε ποσοστό της συνολικής οθόνης και το τοποθετεί στο κέντρο
    def center_window(self, width_factor, height_factor):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        window_width = screen_width * width_factor
        window_height = screen_height * height_factor

        window_pos_x = (screen_width / 2) - (window_width / 2)
        window_pos_y = (screen_height / 2) - (window_height / 2)

        self.root.geometry(
            "%dx%d+%d+%d" % (window_width, window_height, window_pos_x, window_pos_y)
        )
