from ui import Ui
from client_manager import ClientManager

DATABASE_FILE = "app.db"

cli_manager = ClientManager(DATABASE_FILE)

app = Ui(cli_manager)


