from tkinter import Tk
from tkinter import Label
from tkinter import Button
from tkinter import Menu
from tkinter import Frame


class Ui:
    def __init__(self, client_manager):
        self.client_manager = client_manager
        self.window = Tk()
        self.window.title('Appointments Management')
        self.render_menu()
        self.app = Frame(self.window)
        self.app.grid()
        self.window.mainloop()

    def clear_app(self):
        for child in self.app.winfo_children():
            child.destroy()

    def render_menu(self):
        menu = {
            'Αρχείο': self.render_about,
            'Clients': {
                'Add client': self.render_client_form,
                'Delete client': self.render_clients_to_delete,
            },
            'About': self.render_about,
            'Test': self.client_manager.add_test_clients,
        }

        root = Menu()
        for k, v in menu.items():
            if type(v) == dict:
                tmp = Menu()
                for k2, v2 in v.items():
                    tmp.add_command(label=k2, command=v2)
                root.add_cascade(labe=k, menu=tmp)
            else:
                root.add_command(label=k, command=v)
        self.window.config(menu=root)

    def render_client_form(self):
        self.clear_app()
        self.test = Label(self.app, text='hello').grid()
        self.test = Label(self.app, text='test').grid()

    def render_clients_to_delete(self):
        self.clear_app()

        def delete_client(self, id):
            def inner():
                self.client_manager.delete_client(id)
                self.render_clients_to_delete()

            return inner

        for i, client in enumerate(self.client_manager.get_all_clients()):
            Label(
                self.app,
                text=f'{client[0]} {client[1]} {client[2]} {client[3]}',
            ).grid(row=i, column=0)
            Button(
                self.app,
                text='delete',
                command=delete_client(client[0]),
            ).grid(row=i, column=1)

    def render_about(self):
        self.clear_app()
        Label(
            self.app,
            text='SchedulEase\nVersion 0.1\n\nΠΛΗΠΡΟ - ΗΛΕ45'
            '\n\n\nΟΜΑΔΑ\nΓαλατσάνος Δημήτριος\nΛόλας Ιωάννης\nΜορτόπουλος Αγησίλαος'
            '\nΧαλίδου Μαρία\nΚουτσουρίδης Ανέστης',
        ).grid(column=0, row=0)
