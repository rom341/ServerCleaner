import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
from Forms.template_editor import TemplateEditor


class TemplateManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Template Manager")
        self.root.geometry("900x600")
        self.templates = []
        
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

    def update_template_list(self):
        for widget in self.inner_frame.winfo_children():
            widget.destroy()

        for template in self.templates:
            container = ttk.Frame(self.inner_frame)
            container.pack(fill=tk.X, padx=5, pady=5)

            label_name = ttk.Label(container, text=template.owner)
            label_name.pack(side=tk.LEFT, padx=5)

            label_description = ttk.Label(container, text=template.description)
            label_description.pack(side=tk.LEFT, padx=5)

            edit_button = ttk.Button(container, text="Edit", command=lambda t=template: self.edit_selected_template(t))
            edit_button.pack(side=tk.RIGHT, padx=5)

            delete_button = ttk.Button(container, text="Delete", command=lambda t=template: self.delete_selected_template(t))
            delete_button.pack(side=tk.RIGHT, padx=5)

    def open_template_editor(self, template=None):
        def on_template_saved(new_template):
            if new_template:
                if template:
                    idx = self.templates.index(template)
                    self.templates[idx] = new_template
                else:
                    self.templates.append(new_template)
                self.update_template_list()

        self.template_editor = TemplateEditor(self.root, on_template_saved, template)
        self.template_editor.run()
        self.template_editor.editor.wait_window()

    def create_template(self):
        self.open_template_editor()
        self.update_template_list()

    def edit_selected_template(self, template):
        self.open_template_editor(template)
        self.update_template_list()

    def delete_selected_template(self, template):
        selected = template
        self.templates.remove(selected)
        self.update_template_list()

    