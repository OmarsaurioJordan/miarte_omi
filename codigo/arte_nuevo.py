import json
import os
import shutil
import uuid
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

APP_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.abspath(os.path.join(APP_DIR, os.pardir))
MIARTE_DIR = os.path.join(ROOT_DIR, "miarte")
ORIGEN_DIR = os.path.join(ROOT_DIR, "origen")
STYLE_OPTIONS = [
    "sketch",
    "vectorial",
    "ilustración",
    "sprite",
    "asset",
    "tradicional",
    "pixelart",
    "lowdigital",
    "modelo3D",
    "manualidad",
    "fotografía",
    "animación",
    "procedural",
    "textura",
    "editor",
    "mixto",
    "otro",
]
IMAGE_EXTENSIONS = ("png", "jpg", "jpeg", "gif", "bmp", "webm", "svg")


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

def list_folders():
    if not os.path.exists(MIARTE_DIR):
        os.makedirs(MIARTE_DIR, exist_ok=True)
    return sorted(
        [name for name in os.listdir(MIARTE_DIR) if os.path.isdir(os.path.join(MIARTE_DIR, name))]
    )

def make_unique_name(dest_dir, basename):
    base, ext = os.path.splitext(basename)
    candidate = basename
    counter = 1
    while os.path.exists(os.path.join(dest_dir, candidate)):
        candidate = f"{base}_{counter}{ext}"
        counter += 1
    return candidate

def load_data_file(folder_name):
    path = os.path.join(MIARTE_DIR, folder_name, "data.json")
    if not os.path.exists(path):
        return {"title": folder_name, "description": "", "file": "", "series": []}
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

def parse_tags(text):
    return [tag.strip() for tag in text.split(",") if tag.strip()]

def make_unique_id(title):
    slug = title.lower().replace(" ", "_")
    return f"{slug}_{uuid.uuid4().hex}"

class ArteNuevoApp:
    def __init__(self):
        self.selected_images = []
        self.root = create_window("MiArte Omi - Nuevo dibujo", "760x640")
        self.folder_var = tk.StringVar()
        self.title_var = tk.StringVar()
        self.year_var = tk.StringVar()
        self.tags_var = tk.StringVar()
        self.style_var = tk.StringVar(value=STYLE_OPTIONS[0])
        self.nsfw_var = tk.BooleanVar(value=False)
        self.description_text = None
        self.folder_combo = None
        self.images_listbox = None
        self.build_ui()

    def build_ui(self):
        frame = ttk.Frame(self.root, padding=14)
        frame.pack(fill="both", expand=True)

        heading = ttk.Label(frame, text="Nuevo conjunto de dibujos", font=("Segoe UI", 18, "bold"))
        heading.pack(pady=(0, 12))

        controls = ttk.Frame(frame)
        controls.pack(fill="x", pady=8)

        select_button = ttk.Button(controls, text="Seleccionar imágenes", command=self.select_files)
        select_button.grid(row=0, column=0, sticky="w")

        remove_button = ttk.Button(controls, text="Eliminar selección", command=self.remove_selected_image)
        remove_button.grid(row=0, column=1, sticky="w", padx=8)

        move_up_button = ttk.Button(controls, text="Up", command=self.move_image_up)
        move_up_button.grid(row=0, column=2, sticky="w", padx=4)

        move_down_button = ttk.Button(controls, text="Do", command=self.move_image_down)
        move_down_button.grid(row=0, column=3, sticky="w", padx=4)

        controls.columnconfigure(4, weight=1)

        save_button = ttk.Button(controls, text="Guardar", command=self.save)
        save_button.grid(row=0, column=5, sticky="w", padx=8)

        list_frame = ttk.LabelFrame(frame, text="Imágenes seleccionadas")
        list_frame.pack(fill="both", expand=True, pady=8)

        self.images_listbox = tk.Listbox(list_frame, height=5, selectmode=tk.SINGLE)
        self.images_listbox.pack(fill="both", expand=True, padx=8, pady=8)

        form_frame = ttk.LabelFrame(frame, text="Metadatos")
        form_frame.pack(fill="both", expand=True, pady=8)

        labels = ["Folder:", "Título:", "Año:", "Tags:", "Estilo:", "NSFW:"]
        for index, label_text in enumerate(labels):
            label = ttk.Label(form_frame, text=label_text)
            label.grid(row=index, column=0, sticky="e", pady=6, padx=6)

        self.folder_combo = ttk.Combobox(form_frame, textvariable=self.folder_var, values=list_folders(), state="readonly")
        self.folder_combo.grid(row=0, column=1, sticky="we", padx=6, pady=6)
        initial_folder = self.folder_combo['values'][0] if self.folder_combo['values'] else ""
        self.folder_combo.set(initial_folder)
        self.folder_var.set(initial_folder)

        ttk.Entry(form_frame, textvariable=self.title_var, width=56).grid(row=1, column=1, sticky="we", padx=6, pady=6)
        ttk.Entry(form_frame, textvariable=self.year_var, width=56).grid(row=2, column=1, sticky="we", padx=6, pady=6)
        ttk.Entry(form_frame, textvariable=self.tags_var, width=56).grid(row=3, column=1, sticky="we", padx=6, pady=6)
        ttk.Combobox(form_frame, textvariable=self.style_var, values=STYLE_OPTIONS, state="readonly", width=53).grid(row=4, column=1, sticky="we", padx=6, pady=6)
        ttk.Checkbutton(form_frame, text="NSFW", variable=self.nsfw_var).grid(row=5, column=1, sticky="w", padx=6, pady=6)

        description_label = ttk.Label(form_frame, text="Descripción:")
        description_label.grid(row=6, column=0, sticky="ne", pady=6, padx=6)
        self.description_text = tk.Text(form_frame, width=60, height=6, wrap="word")
        self.description_text.grid(row=6, column=1, sticky="we", padx=6, pady=6)

    def select_files(self):
        initial = ORIGEN_DIR if os.path.isdir(ORIGEN_DIR) else ROOT_DIR
        pattern = " ".join(f"*.{ext}" for ext in IMAGE_EXTENSIONS)
        file_paths = filedialog.askopenfilenames(
            title="Seleccionar imágenes",
            initialdir=initial,
            filetypes=[("Imágenes", pattern)],
        )
        for path in file_paths:
            if path and path.lower().endswith(IMAGE_EXTENSIONS) and path not in self.selected_images:
                self.selected_images.append(path)
                self.images_listbox.insert(tk.END, os.path.basename(path))

    def remove_selected_image(self):
        selection = self.images_listbox.curselection()
        if not selection:
            return
        index = selection[0]
        self.images_listbox.delete(index)
        self.selected_images.pop(index)

    def move_image_up(self):
        selection = self.images_listbox.curselection()
        if not selection:
            return
        index = selection[0]
        if index > 0:
            self.selected_images[index], self.selected_images[index - 1] = self.selected_images[index - 1], self.selected_images[index]
            self.refresh_images_listbox()
            self.images_listbox.selection_set(index - 1)

    def move_image_down(self):
        selection = self.images_listbox.curselection()
        if not selection:
            return
        index = selection[0]
        if index < len(self.selected_images) - 1:
            self.selected_images[index], self.selected_images[index + 1] = self.selected_images[index + 1], self.selected_images[index]
            self.refresh_images_listbox()
            self.images_listbox.selection_set(index + 1)

    def refresh_images_listbox(self):
        self.images_listbox.delete(0, tk.END)
        for image_path in self.selected_images:
            self.images_listbox.insert(tk.END, os.path.basename(image_path))

    def save(self):
        if not self.selected_images:
            messagebox.showwarning("Guardar", "Debe seleccionar al menos una imagen.")
            return

        folder_name = self.folder_var.get().strip() or self.folder_combo.get().strip()
        if not folder_name:
            messagebox.showwarning("Guardar", "Seleccione una carpeta de destino.")
            return

        title = self.title_var.get().strip()
        description = self.description_text.get("1.0", tk.END).strip()
        year = self.year_var.get().strip()
        tags = parse_tags(self.tags_var.get())
        style = self.style_var.get().strip()
        nsfw = self.nsfw_var.get()

        if not title:
            messagebox.showwarning("Guardar", "Ingrese un título para la serie.")
            return

        if year and not year.isdigit():
            messagebox.showwarning("Guardar", "El campo año debe ser numérico.")
            return

        folder_path = os.path.join(MIARTE_DIR, folder_name)
        os.makedirs(folder_path, exist_ok=True)

        data = load_data_file(folder_name)
        target_files = []
        for source_path in self.selected_images:
            basename = os.path.basename(source_path)
            destination_name = make_unique_name(folder_path, basename)
            destination_path = os.path.join(folder_path, destination_name)
            try:
                shutil.move(source_path, destination_path)
            except Exception:
                shutil.copy2(source_path, destination_path)
            target_files.append(destination_name)

        series_id = make_unique_id(title)
        new_series = {
            "id": series_id,
            "title": title,
            "description": description,
            "year": int(year) if year.isdigit() else None,
            "tags": tags,
            "nsfw": nsfw,
            "files": target_files,
            "style": style,
        }

        data_series = data.setdefault("series", [])
        data_series.append(new_series)
        if not data.get("file") and target_files:
            data["file"] = target_files[0]

        save_data_file(folder_name, data)
        messagebox.showinfo("Guardado", f"Serie guardada correctamente en {folder_name}.")
        self.close_window()

    def close_window(self):
        if self.root and self.root.winfo_exists():
            self.root.destroy()

def run():
    app = ArteNuevoApp()
    if not app.root._is_toplevel:
        app.root.mainloop()

if __name__ == "__main__":
    run()
