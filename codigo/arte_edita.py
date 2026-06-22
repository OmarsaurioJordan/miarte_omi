import copy
import json
import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

APP_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.abspath(os.path.join(APP_DIR, os.pardir))
MIARTE_DIR = os.path.join(ROOT_DIR, "miarte")
ORIGEN_DIR = os.path.join(ROOT_DIR, "origen")
PAPELERA_DIR = os.path.join(ROOT_DIR, "papelera")
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
IMAGE_EXTENSIONS = ("png", "jpg", "jpeg", "gif", "bmp", "webm")

def list_folders():
    if not os.path.exists(MIARTE_DIR):
        os.makedirs(MIARTE_DIR, exist_ok=True)
    return sorted(
        [name for name in os.listdir(MIARTE_DIR) if os.path.isdir(os.path.join(MIARTE_DIR, name))]
    )

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

def make_unique_name(dest_dir, basename):
    base, ext = os.path.splitext(basename)
    candidate = basename
    counter = 1
    while os.path.exists(os.path.join(dest_dir, candidate)):
        candidate = f"{base}_{counter}{ext}"
        counter += 1
    return candidate

def ensure_papelera():
    os.makedirs(PAPELERA_DIR, exist_ok=True)


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


class ArteEditaApp:
    def __init__(self):
        self.root = create_window("MiArte Omi - Editar dibujo", "920x700")

        self.current_folder = None
        self.current_data = None
        self.series_items = []
        self.current_series = None
        self.original_series = None
        self.selected_images = []

        self.folder_var = tk.StringVar()
        self.title_var = tk.StringVar()
        self.year_var = tk.StringVar()
        self.tags_var = tk.StringVar()
        self.style_var = tk.StringVar(value=STYLE_OPTIONS[0])
        self.nsfw_var = tk.BooleanVar(value=False)
        self.description_text = None
        self.series_listbox = None
        self.images_listbox = None
        self.folder_combo = None
        self.folder_select = None
        self.current_folder_label = None
        self.build_ui()

    def build_ui(self):
        frame = ttk.Frame(self.root, padding=12)
        frame.pack(fill="both", expand=True)

        heading = ttk.Label(frame, text="Editar serie de dibujos", font=("Segoe UI", 18, "bold"))
        heading.pack(pady=(0, 10))

        top_frame = ttk.Frame(frame)
        top_frame.pack(fill="x", pady=6)

        folder_label = ttk.Label(top_frame, text="Carpeta:")
        folder_label.pack(side="left")

        self.folder_select = ttk.Combobox(top_frame, values=list_folders(), state="readonly", width=36)
        self.folder_select.pack(side="left", padx=(6, 0))
        self.folder_select.bind("<<ComboboxSelected>>", self.on_folder_select)

        self.current_folder_label = ttk.Label(top_frame, text="Carpeta: ninguna", foreground="blue")
        self.current_folder_label.pack(side="left", padx=12)

        body_frame = ttk.Frame(frame)
        body_frame.pack(fill="both", expand=True, pady=10)

        left_panel = ttk.Frame(body_frame)
        left_panel.pack(side="left", fill="y", padx=(0, 12))

        series_frame = ttk.LabelFrame(left_panel, text="Series disponibles")
        series_frame.pack(fill="y", expand=True)

        self.series_listbox = tk.Listbox(series_frame, width=40, height=24)
        self.series_listbox.pack(fill="both", expand=True, padx=8, pady=8)
        self.series_listbox.bind("<<ListboxSelect>>", self.on_series_select)

        right_panel = ttk.Frame(body_frame)
        right_panel.pack(side="left", fill="both", expand=True)

        form_frame = ttk.LabelFrame(right_panel, text="Metadatos")
        form_frame.pack(fill="x", pady=6)

        labels = ["Folder:", "ID:", "Título:", "Año:", "Tags:", "Estilo:", "NSFW:"]
        for index, label_text in enumerate(labels):
            label = ttk.Label(form_frame, text=label_text)
            label.grid(row=index, column=0, sticky="e", pady=6, padx=6)

        self.folder_combo = ttk.Combobox(form_frame, textvariable=self.folder_var, values=list_folders(), state="readonly", width=44)
        self.folder_combo.grid(row=0, column=1, sticky="we", padx=6, pady=6)

        self.id_label = ttk.Label(form_frame, text="-")
        self.id_label.grid(row=1, column=1, sticky="w", padx=6, pady=6)

        ttk.Entry(form_frame, textvariable=self.title_var, width=56).grid(row=2, column=1, sticky="we", padx=6, pady=6)
        ttk.Entry(form_frame, textvariable=self.year_var, width=56).grid(row=3, column=1, sticky="we", padx=6, pady=6)
        ttk.Entry(form_frame, textvariable=self.tags_var, width=56).grid(row=4, column=1, sticky="we", padx=6, pady=6)
        ttk.Combobox(form_frame, textvariable=self.style_var, values=STYLE_OPTIONS, state="readonly", width=53).grid(row=5, column=1, sticky="we", padx=6, pady=6)
        ttk.Checkbutton(form_frame, text="NSFW", variable=self.nsfw_var).grid(row=6, column=1, sticky="w", padx=6, pady=6)

        description_label = ttk.Label(form_frame, text="Descripción:")
        description_label.grid(row=7, column=0, sticky="ne", pady=6, padx=6)
        self.description_text = tk.Text(form_frame, width=60, height=6, wrap="word")
        self.description_text.grid(row=7, column=1, sticky="we", padx=6, pady=6)

        image_frame = ttk.LabelFrame(right_panel, text="Imágenes actuales")
        image_frame.pack(fill="both", expand=True, pady=8)

        button_frame = ttk.Frame(image_frame)
        button_frame.pack(fill="x", padx=8, pady=(8, 4))

        add_button = ttk.Button(button_frame, text="Seleccionar imágenes", command=self.add_files)
        add_button.grid(row=0, column=0, sticky="w")

        remove_button = ttk.Button(button_frame, text="Eliminar selección", command=self.remove_selected_image)
        remove_button.grid(row=0, column=1, sticky="w", padx=(4, 4))

        move_up_button = ttk.Button(button_frame, text="Up", command=self.move_image_up)
        move_up_button.grid(row=0, column=2, sticky="w", padx=4)

        move_down_button = ttk.Button(button_frame, text="Do", command=self.move_image_down)
        move_down_button.grid(row=0, column=3, sticky="w", padx=4)

        spacer = ttk.Label(button_frame, text="")
        spacer.grid(row=0, column=4, sticky="ew")
        button_frame.columnconfigure(4, weight=1)

        save_button = ttk.Button(button_frame, text="Guardar", command=self.save)
        save_button.grid(row=0, column=5, sticky="e")

        self.images_listbox = tk.Listbox(image_frame, width=60, height=12, selectmode=tk.SINGLE)
        self.images_listbox.pack(fill="both", expand=True, padx=8, pady=8)

    def on_folder_select(self, event=None):
        folder_name = self.folder_select.get().strip()
        if not folder_name:
            return
        if folder_name not in list_folders():
            messagebox.showwarning("Carpeta inválida", "Seleccione una carpeta válida dentro de miarte/.")
            return
        self.current_folder = folder_name
        self.current_folder_label.config(text=f"Carpeta: {self.current_folder}")

        self.current_series = None
        self.original_series = None
        self.series_listbox.delete(0, tk.END)
        self.id_label.config(text="-")
        self.folder_var.set("")
        self.title_var.set("")
        self.year_var.set("")
        self.tags_var.set("")
        self.style_var.set(STYLE_OPTIONS[0])
        self.nsfw_var.set(False)
        self.description_text.delete("1.0", tk.END)
        self.selected_images = []
        self.images_listbox.delete(0, tk.END)

        self.current_data = load_data_file(self.current_folder)
        self.series_items = self.current_data.get("series", [])
        self.populate_series_listbox()
        self.folder_combo.config(values=list_folders())
        if self.current_folder not in self.folder_combo['values']:
            self.folder_combo['values'] = list(self.folder_combo['values']) + [self.current_folder]
        self.folder_combo.set(self.current_folder)

    def populate_series_listbox(self):
        self.series_listbox.delete(0, tk.END)
        for item in self.series_items:
            title = item.get("title", "<sin título>")
            series_id = item.get("id", "-")
            self.series_listbox.insert(tk.END, f"{title} ({series_id})")

    def on_series_select(self, event=None):
        selection = self.series_listbox.curselection()
        if not selection:
            return
        index = selection[0]
        self.current_series = self.series_items[index]
        self.original_series = copy.deepcopy(self.current_series)
        self.folder_var.set(self.current_folder or "")
        self.id_label.config(text=self.current_series.get("id", "-"))
        self.title_var.set(self.current_series.get("title", ""))
        self.year_var.set(str(self.current_series.get("year", "")))
        self.tags_var.set(", ".join(self.current_series.get("tags", [])))
        self.style_var.set(self.current_series.get("style", STYLE_OPTIONS[0]))
        self.nsfw_var.set(bool(self.current_series.get("nsfw", False)))
        self.description_text.delete("1.0", tk.END)
        self.description_text.insert(tk.END, self.current_series.get("description", ""))
        self.selected_images = []
        self.images_listbox.delete(0, tk.END)
        series_files = self.current_series.get("files", [])
        folder_path = os.path.join(MIARTE_DIR, self.current_folder)
        for filename in series_files:
            source_path = os.path.join(folder_path, filename)
            if os.path.exists(source_path):
                self.selected_images.append(source_path)
                self.images_listbox.insert(tk.END, filename)
            else:
                self.images_listbox.insert(tk.END, f"{filename} (no existe)")

    def add_files(self):
        initial = ORIGEN_DIR if os.path.isdir(ORIGEN_DIR) else ROOT_DIR
        file_paths = filedialog.askopenfilenames(
            title="Seleccionar imágenes",
            initialdir=initial,
            filetypes=[("Imágenes", "*.png *.jpg *.jpeg *.gif *.bmp *.webm")],
        )
        for path in file_paths:
            if path and path.lower().endswith(IMAGE_EXTENSIONS):
                if path not in self.selected_images:
                    self.selected_images.append(path)
                    self.images_listbox.insert(tk.END, os.path.basename(path))

    def remove_selected_image(self):
        selection = self.images_listbox.curselection()
        if not selection:
            return
        index = selection[0]
        self.selected_images.pop(index)
        self.images_listbox.delete(index)

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
            filename = os.path.basename(image_path)
            if os.path.exists(image_path):
                self.images_listbox.insert(tk.END, filename)
            else:
                self.images_listbox.insert(tk.END, f"{filename} (no existe)")

    def save(self):
        if not self.current_series:
            messagebox.showwarning("Guardar", "Seleccione una serie para editar.")
            return

        folder_name = self.folder_var.get().strip()
        if not folder_name:
            messagebox.showwarning("Guardar", "Seleccione una carpeta de destino.")
            return

        title = self.title_var.get().strip()
        if not title:
            messagebox.showwarning("Guardar", "Ingrese un título.")
            return

        year = self.year_var.get().strip()
        if year and not year.isdigit():
            messagebox.showwarning("Guardar", "El campo año debe ser numérico.")
            return

        description = self.description_text.get("1.0", tk.END).strip()
        tags = parse_tags(self.tags_var.get())
        style = self.style_var.get().strip() or STYLE_OPTIONS[0]
        nsfw = self.nsfw_var.get()

        source_folder = self.current_folder
        target_folder = folder_name
        old_id = self.current_series.get("id")

        source_data = load_data_file(source_folder)
        target_data = load_data_file(target_folder)
        os.makedirs(os.path.join(MIARTE_DIR, target_folder), exist_ok=True)
        ensure_papelera()

        original_files = [f for f in self.original_series.get("files", [])]
        current_names = [os.path.basename(path) for path in self.selected_images]
        removed_files = [f for f in original_files if f not in current_names]

        final_names = []
        for source_path in self.selected_images:
            basename = os.path.basename(source_path)
            target_path = os.path.join(MIARTE_DIR, target_folder, basename)
            if os.path.abspath(source_path) == os.path.abspath(target_path):
                final_names.append(basename)
                continue
            destination = os.path.join(MIARTE_DIR, target_folder, make_unique_name(os.path.join(MIARTE_DIR, target_folder), basename))
            try:
                shutil.move(source_path, destination)
            except Exception:
                shutil.copy2(source_path, destination)
            final_names.append(os.path.basename(destination))

        for removed_name in removed_files:
            removed_path = os.path.join(MIARTE_DIR, source_folder, removed_name)
            if os.path.exists(removed_path):
                destination = os.path.join(PAPELERA_DIR, make_unique_name(PAPELERA_DIR, removed_name))
                shutil.move(removed_path, destination)

        new_series = {
            "id": old_id,
            "title": title,
            "description": description,
            "year": int(year) if year.isdigit() else None,
            "tags": tags,
            "nsfw": nsfw,
            "files": final_names,
            "style": style,
        }

        if source_folder != target_folder:
            source_data["series"] = [item for item in source_data.get("series", []) if item.get("id") != old_id]
            save_data_file(source_folder, source_data)
            target_series = [item for item in target_data.setdefault("series", []) if item.get("id") != old_id]
            target_series.append(new_series)
            target_data["series"] = target_series
            if not target_data.get("file") and final_names:
                target_data["file"] = final_names[0]
            save_data_file(target_folder, target_data)
        else:
            series_list = source_data.get("series", [])
            for index, item in enumerate(series_list):
                if item.get("id") == old_id:
                    series_list[index] = new_series
                    break
            source_data["series"] = series_list
            if not source_data.get("file") and final_names:
                source_data["file"] = final_names[0]
            save_data_file(source_folder, source_data)

        if not final_names:
            messagebox.showinfo("Guardado", "No había archivos en la serie; la metadata fue eliminada y los dibujos eliminados a la papelera.")
        else:
            messagebox.showinfo("Guardado", "La serie se actualizó correctamente.")
        self.close_window()

    def close_window(self):
        if self.root and self.root.winfo_exists():
            self.root.destroy()

def run():
    app = ArteEditaApp()
    if not app.root._is_toplevel:
        app.root.mainloop()

if __name__ == "__main__":
    run()
