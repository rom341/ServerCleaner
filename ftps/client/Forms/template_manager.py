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

        self.template_listbox = tk.Listbox(self.frame)
        self.template_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scrollbar = ttk.Scrollbar(self.frame, orient=tk.VERTICAL, command=self.template_listbox.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.template_listbox.config(yscrollcommand=self.scrollbar.set)

        self.add_button = ttk.Button(root, text="Add Template", command=lambda: self.open_template_editor())
        self.add_button.pack(pady=5)

        self.edit_button = ttk.Button(root, text="Edit Selected Template", command=self.edit_selected_template)
        self.edit_button.pack(pady=5)

    def open_template_editor(self, template=None):
        self.template_editor = TemplateEditor(self.root, self.templates, self.template_listbox, template)
        self.template_editor.run()

    def edit_selected_template(self):
        selected = self.template_listbox.curselection()
        if selected:
            idx = selected[0]
            template = self.templates[idx]
            self.open_template_editor(template)
        else:
            messagebox.showinfo("Info", "Please select a template to edit.")

    