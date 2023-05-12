from ui import Ui
from client_manager import ClientManager
from appointment_manager import AppointmentManager
from employee_manager import EmployeeManager
from utils import *
from datetime import datetime

DATABASE_FILE = "app.db"

client_manager = ClientManager(DATABASE_FILE)
appointment_manager = AppointmentManager(DATABASE_FILE)
employee_manager = EmployeeManager(DATABASE_FILE)

app = Ui(client_manager)

# TEST ACCOUNT ('dr.georgepapadopoulos@gmail.com', 'sphgkfocygdxfneu')

