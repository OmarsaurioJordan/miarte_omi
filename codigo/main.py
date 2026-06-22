import os
import sys
import tkinter as tk
from tkinter import ttk, messagebox

# obtenemos el directorio del codigo y del proyecto, luego agrega el directorio al path de importaciones
APP_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.abspath(os.path.join(APP_DIR, os.pardir))
sys.path.insert(0, APP_DIR)

def open_script(module_name):
    # para ejecutar scripts python desde el main, deben tener run()
    try:
        module = __import__(module_name)
        if hasattr(module, "run"):
            module.run()
        else:
            messagebox.showerror("Error", f"El módulo {module_name} no tiene función run().")
    except Exception as exc:
        messagebox.showerror("Error", f"No se pudo abrir {module_name}: {exc}")

def run():
    os.chdir(ROOT_DIR)
    root = tk.Tk()
    root.title("MiArte Omi")
    root.geometry("480x330")
    root.resizable(True, True)

    frame = ttk.Frame(root, padding=16)
    frame.pack(fill="both", expand=True)

    title = ttk.Label(frame, text="MiArte Omi", font=("Segoe UI", 20, "bold"))
    title.pack(pady=(0, 12))

    subtitle = ttk.Label(
        frame,
        text=(
            "Administrador de dibujos por Omwekiatl 2026\n"
            "Use Nuevo para importar dibujos y asignar metadatos\n"
            "Use Editar para modificar dibujos guardados y sus metadatos\n"
            "Use Generar para crear el sitio web mediante plantillas HTML"
        ),
        justify="center",
    )
    subtitle.pack(pady=(0, 18))

    button_frame = ttk.Frame(frame)
    button_frame.pack(pady=8)

    nuevo_button = ttk.Button(button_frame, text="Nuevo", width=16, command=lambda: open_script("arte_nuevo"))
    nuevo_button.grid(row=0, column=0, padx=8, pady=4)

    editar_button = ttk.Button(button_frame, text="Editar", width=16, command=lambda: open_script("arte_edita"))
    editar_button.grid(row=1, column=0, padx=8, pady=4)

    generar_button = ttk.Button(button_frame, text="Generar", width=16, command=lambda: open_script("genera_html"))
    generar_button.grid(row=2, column=0, padx=8, pady=4)

    about_label = ttk.Label(
        frame,
        text=(
            "Diseñado para organizar colecciones de dibujos y generar un sitio web estático.\n"
            "Permite guardar todo en un repositorio, a la vez que editar los datos en local.\n"
            "Coloque las imágenes originales en la carpeta origen/ y luego use el editor.\n"
            "Los datos se almacenan en las carpetas de miarte/ y los metadatos en archivos JSON."
        ),
        wraplength=420,
        justify="center",
    )
    about_label.pack(pady=(18, 0))

    root.mainloop()

if __name__ == "__main__":
    run()
