import tkinter as tk
from Forms.template_manager import TemplateManagerApp
from ftps.Data.Repositories.db_connection import DBConnection
from ftps.Data.template import Template
from ftps.Data.user import User

if __name__ == "__main__":
    connection_str = "sqlite:///ftps/client/Config/client_templates.db"
    connection = DBConnection(connection_str)

    root = tk.Tk()
    app = TemplateManagerApp(root, connection)
    root.mainloop()
    connection.close_session()