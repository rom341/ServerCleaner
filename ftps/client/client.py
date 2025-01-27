import tkinter as tk
from Forms.template_manager import TemplateManagerApp
from ftps.Data.Repositories.db_connection import DBConnection
from ftps.Data.config_reader import ConfigReader

if __name__ == "__main__":
    configReader = ConfigReader("ftps/client/Config/clientData.conf")
    connectionString = configReader.get("saves_db", "connection_string")
    connection = DBConnection(connectionString)

    root = tk.Tk()
    app = TemplateManagerApp(root, connection, configReader)
    root.mainloop()
    connection.close_session()