import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
from Forms.template_editor import TemplateEditor
from ftps.Data.Repositories import db_connection
from ftps.Data.template import Template
from ftps.Data.Repositories.template_repository import TemplateRepository

class TemplateManagerApp:
    def __init__(self, root, db_connection):
        self.root = root
        self.root.title("Template Manager")
        self.root.geometry("900x600")
        
        # Создаём экземпляр репозитория
        self.db_connection = db_connection
        self.template_repo = TemplateRepository(self.db_connection)

        # Main UI Layout
        self.frame = ttk.Frame(root)
        self.frame.pack(fill=tk.BOTH, expand=True)

        # Scrollable container
        self.canvas = tk.Canvas(self.frame)
        self.scrollbar = ttk.Scrollbar(self.frame, orient=tk.VERTICAL, command=self.canvas.yview)
        self.inner_frame = ttk.Frame(self.canvas)

        self.inner_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.inner_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.add_button = ttk.Button(root, text="Add Template", command=self.create_template)
        self.add_button.pack(pady=5)

        self.update_gui_template_list()

    def update_gui_template_list(self):
        for widget in self.inner_frame.winfo_children():
            widget.destroy()

        templates = self.template_repo.get_all_templates()

        for template in templates:
            container = ttk.Frame(self.inner_frame)
            container.pack(fill=tk.X, padx=5, pady=5)

            label_name = ttk.Label(container, text=template.owner.name, width=15, anchor="w")
            label_name.grid(row=0, column=0, padx=5, pady=2, sticky="w")

            label_description = ttk.Label(container, text=template.description, width=60, anchor="w")
            label_description.grid(row=0, column=1, padx=5, pady=2, sticky="w")

            edit_button = ttk.Button(container, text="Edit", command=lambda t=template: self.edit_selected_template(t))
            edit_button.grid(row=0, column=2, padx=5, pady=2, sticky="e")

            delete_button = ttk.Button(container, text="Delete", command=lambda t=template: self.delete_selected_template(t))
            delete_button.grid(row=0, column=3, padx=5, pady=2, sticky="e")

            container.grid_columnconfigure(0, weight=1)
            container.grid_columnconfigure(1, weight=2)

    def open_template_editor(self, template=None):
        def on_template_saved(new_template):
            if new_template:
                if template:
                    self.template_repo.update_template(template.id, {
                        "description": new_template.description,
                        "paths": new_template.client_server_paths,
                        "ttl_default": new_template.ttl_default,
                        "keep_alive": new_template.keep_alive,
                        "keep_alive_timer": new_template.keep_alive_timer,
                        "keep_alive_increment": new_template.keep_alive_increment,
                    })
                else:
                    self.template_repo.create_template(new_template)
                self.update_gui_template_list()

        self.template_editor = TemplateEditor(self.root, self.db_connection, on_template_saved, template)
        self.template_editor.run()
        self.template_editor.editor.wait_window()

    def create_template(self):
        self.open_template_editor()
        self.update_gui_template_list()

    def edit_selected_template(self, template):
        self.open_template_editor(template)
        self.update_gui_template_list()

    def delete_selected_template(self, template):
        if messagebox.askyesno("Delete Template", "Are you sure you want to delete this template?"):
            self.template_repo.delete_template(template.id)
            self.update_gui_template_list()
