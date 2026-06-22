import json
import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

APP_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.abspath(os.path.join(APP_DIR, os.pardir))
MIARTE_DIR = os.path.join(ROOT_DIR, "miarte")
ORIGEN_DIR = os.path.join(ROOT_DIR, "origen")
IMAGE_EXTENSIONS = ("png", "jpg", "jpeg", "gif", "bmp", "webm", "svg")

def list_folders():
    if not os.path.exists(MIARTE_DIR):
        os.makedirs(MIARTE_DIR, exist_ok=True)
    return sorted(
        [name for name in os.listdir(MIARTE_DIR) if os.path.isdir(os.path.join(MIARTE_DIR, name))]
    )

def load_data_file(folder_name):
    path = os.path.join(MIARTE_DIR, folder_name, "data.json")
    if not os.path.exists(path):
        data = {"title": folder_name, "description": "", "file": "", "series": []}
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as handle:
            json.dump(data, handle, indent=2, ensure_ascii=False)
        return data
    with open(path, "r", encoding="utf-8") as handle:
        try:
            data = json.load(handle)
        except json.JSONDecodeError:
            data = {}
    data.setdefault("title", folder_name)
    data.setdefault("description", "")
    data.setdefault("file", "")
    data.setdefault("series", [])
    return data

def save_data_file(folder_name, data):
    path = os.path.join(MIARTE_DIR, folder_name, "data.json")
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(data, handle, indent=2, ensure_ascii=False)

def create_window(title, size):
    is_toplevel = bool(tk._default_root)
    if is_toplevel:
        root = tk.Toplevel(tk._default_root)
        root.transient(tk._default_root)
        root.grab_set()
        root.focus_force()
    else:
        root = tk.Tk()
    root._is_toplevel = is_toplevel
    root.title(title)
    root.geometry(size)
    root.resizable(True, True)
    root.protocol("WM_DELETE_WINDOW", root.destroy)
    return root

class GrupoEditaApp:
    def __init__(self):
        self.root = create_window("MiArte Omi - Grupos", "840x640")
        self.current_folder = None
        self.current_data = None

        self.title_var = tk.StringVar()
        self.description_text = None
        self.file_var = tk.StringVar()

        self.folder_listbox = None
        self.file_label = None
        self.build_ui()
        self.load_folders()

    def build_ui(self):
        frame = ttk.Frame(self.root, padding=12)
        frame.pack(fill="both", expand=True)

        heading = ttk.Label(frame, text="Editar metadatos de carpeta", font=("Segoe UI", 18, "bold"))
        heading.pack(pady=(0, 12))

        body_frame = ttk.Frame(frame)
        body_frame.pack(fill="both", expand=True)

        left_panel = ttk.Frame(body_frame)
        left_panel.pack(side="left", fill="y", padx=(0, 12))

        series_frame = ttk.LabelFrame(left_panel, text="Carpetas en miarte")
        series_frame.pack(fill="both", expand=True)

        self.folder_listbox = tk.Listbox(series_frame, width=36, height=24, selectmode=tk.SINGLE)
        self.folder_listbox.pack(fill="both", expand=True, padx=8, pady=8)
        self.folder_listbox.bind("<<ListboxSelect>>", self.on_folder_select)

        right_panel = ttk.Frame(body_frame)
        right_panel.pack(side="left", fill="both", expand=True)

        form_frame = ttk.LabelFrame(right_panel, text="Metadatos de carpeta")
        form_frame.pack(fill="x", pady=6)

        labels = ["Título:", "Descripción:", "Archivo principal:"]
        for index, label_text in enumerate(labels):
            label = ttk.Label(form_frame, text=label_text)
            label.grid(row=index, column=0, sticky="ne" if index == 1 else "e", pady=6, padx=6)

        ttk.Entry(form_frame, textvariable=self.title_var, width=56).grid(row=0, column=1, sticky="we", padx=6, pady=6)

        self.description_text = tk.Text(form_frame, width=60, height=6, wrap="word")
        self.description_text.grid(row=1, column=1, sticky="we", padx=6, pady=6)

        file_frame = ttk.Frame(form_frame)
        file_frame.grid(row=2, column=1, sticky="we", padx=6, pady=6)

        self.file_label = ttk.Label(file_frame, textvariable=self.file_var, width=44)
        self.file_label.pack(side="left", fill="x", expand=True)

        select_file_button = ttk.Button(file_frame, text="Seleccionar imágenes", command=self.select_file)
        select_file_button.pack(side="left", padx=(8, 0))

        button_frame = ttk.Frame(right_panel)
        button_frame.pack(fill="x", pady=8)

        save_button = ttk.Button(button_frame, text="Guardar", command=self.save)
        save_button.pack(side="right", padx=8)

    def load_folders(self):
        self.folder_listbox.delete(0, tk.END)
        for folder_name in list_folders():
            self.folder_listbox.insert(tk.END, folder_name)

    def on_folder_select(self, event=None):
        selection = self.folder_listbox.curselection()
        if not selection:
            return
        index = selection[0]
        folder_name = self.folder_listbox.get(index)
        self.current_folder = folder_name
        self.current_data = load_data_file(folder_name)
        self.title_var.set(self.current_data.get("title", folder_name))
        self.description_text.delete("1.0", tk.END)
        self.description_text.insert(tk.END, self.current_data.get("description", ""))
        self.file_var.set(self.current_data.get("file", ""))

    def select_file(self):
        if not self.current_folder:
            messagebox.showwarning("Seleccionar imágenes", "Seleccione primero una carpeta.")
            return

        initial_dir = os.path.join(MIARTE_DIR, self.current_folder)
        if not os.path.isdir(initial_dir):
            initial_dir = MIARTE_DIR

        file_paths = filedialog.askopenfilenames(
            title="Seleccionar imágenes",
            initialdir=initial_dir,
            filetypes=[("Imágenes", "*.png *.jpg *.jpeg *.gif *.bmp *.webm *.svg")],
        )
        if not file_paths:
            return

        basename = os.path.basename(file_paths[0])
        self.file_var.set(basename)

    def save(self):
        if not self.current_folder:
            messagebox.showwarning("Guardar", "Seleccione una carpeta para editar.")
            return

        title = self.title_var.get().strip() or self.current_folder
        description = self.description_text.get("1.0", tk.END).strip()
        file_name = self.file_var.get().strip()

        data = load_data_file(self.current_folder)
        data["title"] = title
        data["description"] = description
        data["file"] = file_name
        data.setdefault("series", [])
        save_data_file(self.current_folder, data)

        messagebox.showinfo("Guardado", "Metadatos de carpeta guardados correctamente.")

def run():
    app = GrupoEditaApp()
    app.root.mainloop()

if __name__ == "__main__":
    run()
