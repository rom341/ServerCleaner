import tkinter as tk
from tkinter import ttk, messagebox
from ftps.client.Data.template import Template, ClientServerPathPair

class TemplateEditor:
    def __init__(self, root, templates, template_listbox, template=None):
        self.root = root
        self.template = template
        self.templates = templates
        self.template_listbox = template_listbox
        self.editor = tk.Toplevel(self.root)

    def run(self):
        self.editor.grab_set()
        self.editor.title("Template Editor")
        self.editor.geometry("700x500")

        owner_label = ttk.Label(self.editor, text="Owner:")
        owner_label.pack()
        self.owner_entry = ttk.Entry(self.editor)
        self.owner_entry.pack()

        description_label = ttk.Label(self.editor, text="Description:")
        description_label.pack()
        self.description_entry = ttk.Entry(self.editor)
        self.description_entry.pack()

        ttl_label = ttk.Label(self.editor, text="Default TTL (seconds):")
        ttl_label.pack()
        self.ttl_entry = ttk.Entry(self.editor)
        self.ttl_entry.pack()

        self.keep_alive_var = tk.BooleanVar()
        keep_alive_check = ttk.Checkbutton(self.editor, text="Enable Keep Alive", variable=self.keep_alive_var)
        keep_alive_check.pack()

        keep_alive_timer_label = ttk.Label(self.editor, text="Keep Alive Timer (seconds):")
        keep_alive_timer_label.pack()
        self.keep_alive_timer_entry = ttk.Entry(self.editor)
        self.keep_alive_timer_entry.pack()

        keep_alive_increment_label = ttk.Label(self.editor, text="Keep Alive Increment (seconds):")
        keep_alive_increment_label.pack()
        self.keep_alive_increment_entry = ttk.Entry(self.editor)
        self.keep_alive_increment_entry.pack()

        self.path_frame = ttk.Frame(self.editor)
        self.path_frame.pack(fill=tk.BOTH, expand=True)

        self.path_listbox = ttk.Frame(self.path_frame)
        self.path_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.paths = []

        path_add_button = ttk.Button(self.editor, text="Add Path", command=self.add_path)
        path_add_button.pack(pady=5)

        save_button = ttk.Button(self.editor, text="Save", command=self.save_template)
        save_button.pack(pady=10)

        if self.template:
            self.owner_entry.insert(0, self.template.owner)
            self.description_entry.insert(0, self.template.description)
            self.ttl_entry.insert(0, str(self.template.ttlDefault))
            self.keep_alive_var.set(self.template.keepAlive)
            self.keep_alive_timer_entry.insert(0, str(self.template.keepAliveTimer))
            self.keep_alive_increment_entry.insert(0, str(self.template.keepAliveIncrement))
            self.paths = self.template.clientServerPaths
            for path in self.paths:
                self.create_path_container(self.path_listbox, path, self.paths)

    def add_path(self):
        source, destination = self.path_dialog(self.editor)
        if source and destination:
            path_pair = ClientServerPathPair(source, destination)
            self.paths.append(path_pair)
            self.create_path_container(self.path_listbox, path_pair, self.paths)

    def save_template(self):
        owner = self.owner_entry.get().strip()
        description = self.description_entry.get().strip()
        ttl_str = self.ttl_entry.get().strip()
        keep_alive = self.keep_alive_var.get()
        keep_alive_timer_str = self.keep_alive_timer_entry.get().strip()
        keep_alive_increment_str = self.keep_alive_increment_entry.get().strip()

        if not owner:
            messagebox.showerror("Error", "Owner field cannot be empty.")
            return
        if not ttl_str.isdigit():
            messagebox.showerror("Error", "TTL field must be a valid number.")
            return

        ttl = int(ttl_str) 

        if not keep_alive_timer_str.isdigit():
            messagebox.showerror("Error", "Keep Alive Timer must be a valid number.")
            return
        if not keep_alive_increment_str.isdigit():
            messagebox.showerror("Error", "Keep Alive Increment must be a valid number.")
            return
        
        keep_alive_timer = int(keep_alive_timer_str)
        keep_alive_increment = int(keep_alive_increment_str)
        
        new_template = Template(owner, description, self.paths, ttl, keep_alive, keep_alive_timer, keep_alive_increment)
        self.save_edited_template(self.template, new_template, self.templates, self.template_listbox)
        self.root.destroy()

    def create_path_container(self, parent, path_pair, path_list):
        frame = ttk.Frame(parent)
        frame.pack(fill=tk.X, pady=2)

        source_label = ttk.Label(frame, text=path_pair.source, width=30, anchor="w")
        source_label.pack(side=tk.LEFT, padx=5)

        arrow_label = ttk.Label(frame, text="→", font=("Arial", 12))
        arrow_label.pack(side=tk.LEFT)

        destination_label = ttk.Label(frame, text=path_pair.destination, width=30, anchor="w")
        destination_label.pack(side=tk.LEFT, padx=5)

        def edit_path():
            source, destination = self.path_dialog()
            if source and destination:
                path_pair.source = source
                path_pair.destination = destination
                source_label.config(text=source)
                destination_label.config(text=destination)

        edit_button = ttk.Button(frame, text="Edit", command=edit_path)
        edit_button.pack(side=tk.LEFT, padx=5)

        def remove_path():
            path_list.remove(path_pair)
            frame.destroy()

        remove_button = ttk.Button(frame, text="Remove", command=remove_path)
        remove_button.pack(side=tk.LEFT, padx=5)

    def path_dialog(self, parent, source="", destination=""):
        dialog = tk.Toplevel(parent)
        dialog.title("Input Paths")

        dialog.transient(parent)
        dialog.grab_set() 

        tk.Label(dialog, text="Enter source path:").pack()
        source_entry = ttk.Entry(dialog)
        source_entry.insert(0, source)
        source_entry.pack()

        tk.Label(dialog, text="Enter destination path:").pack()
        destination_entry = ttk.Entry(dialog)
        destination_entry.insert(0, destination)
        destination_entry.pack()

        dialog.geometry("300x150")

        result = []

        def on_submit():
            result.append(source_entry.get())
            result.append(destination_entry.get())
            dialog.destroy()

        submit_button = ttk.Button(dialog, text="Submit", command=on_submit)
        submit_button.pack(pady=5)

        dialog.transient(self.root)
        dialog.wait_window()

        return result[0], result[1]



    def save_edited_template(self, template, new_template, templates, template_listbox):
        if template:
            idx = templates.index(template)
            templates[idx] = new_template
        else:
            templates.append(new_template)
            template_listbox.insert(tk.END, new_template.description)
        messagebox.showinfo("Info", "Template saved successfully.")

