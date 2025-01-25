import tkinter as tk
from Forms.template_manager import TemplateManagerApp
from Data.ftps_client import FtpsClient

if __name__ == "__main__":
    root = tk.Tk()
    app = TemplateManagerApp(root)
    root.mainloop()