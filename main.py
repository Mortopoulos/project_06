from ui import Ui
from client_manager import ClientManager
from appointment_manager import AppointmentManager
from utils import *
from datetime import datetime

DATABASE_FILE = "app.db"

cli_manager = ClientManager(DATABASE_FILE)
appointment_manager = AppointmentManager(DATABASE_FILE)

app = Ui(cli_manager)