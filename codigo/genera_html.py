import json
import os
import shutil
import tkinter as tk
from tkinter import messagebox

APP_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.abspath(os.path.join(APP_DIR, os.pardir))
MIARTE_DIR = os.path.join(ROOT_DIR, "miarte")
WEBSITE_DIR = os.path.join(ROOT_DIR, "website")
ASSETS_DIR = os.path.join(WEBSITE_DIR, "assets")

def load_json(path):
    if not os.path.exists(path):
        return None
    with open(path, "r", encoding="utf-8") as handle:
        try:
            return json.load(handle)
        except json.JSONDecodeError:
            return None

def safe_remove(path):
    if os.path.isdir(path):
        shutil.rmtree(path)
    elif os.path.exists(path):
        os.remove(path)

def generate_site():
    safe_remove(WEBSITE_DIR)
    os.makedirs(ASSETS_DIR, exist_ok=True)

    groups = []
    for folder_name in sorted(os.listdir(MIARTE_DIR)):
        folder_path = os.path.join(MIARTE_DIR, folder_name)
        if not os.path.isdir(folder_path):
            continue
        data_path = os.path.join(folder_path, "data.json")
        data = load_json(data_path) or {"title": folder_name, "description": "", "file": "", "series": []}
        group = {
            "folder": folder_name,
            "title": data.get("title", folder_name),
            "description": data.get("description", ""),
            "series": [],
        }
        asset_folder = os.path.join(ASSETS_DIR, folder_name)
        os.makedirs(asset_folder, exist_ok=True)

        for series in data.get("series", []):
            series_files = []
            for filename in series.get("files", []):
                source = os.path.join(folder_path, filename)
                if os.path.exists(source):
                    target = os.path.join(asset_folder, filename)
                    if not os.path.exists(target):
                        shutil.copy2(source, target)
                    series_files.append(os.path.join("assets", folder_name, filename).replace("\\", "/"))
            group["series"].append({
                "id": series.get("id", ""),
                "title": series.get("title", ""),
                "description": series.get("description", ""),
                "year": series.get("year", ""),
                "tags": series.get("tags", []),
                "nsfw": series.get("nsfw", False),
                "style": series.get("style", ""),
                "files": series_files,
            })
        groups.append(group)

    author_data = load_json(os.path.join(ROOT_DIR, "autor.json")) or {}
    title = author_data.get("nickname", "MiArte Omi")
    author_name = author_data.get("name", "Autor")
    author_description = author_data.get("description", "Colección de arte.")

    html = [
        "<!DOCTYPE html>",
        "<html lang=\"es\">",
        "<head>",
        f"<meta charset=\"UTF-8\">",
        f"<meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">",
        f"<title>{title}</title>",
        "<style>",
        "body{font-family:Segoe UI, sans-serif;margin:0;padding:0;background:#f9f9f9;color:#222}",
        "header{background:#333;color:#fff;padding:24px 30px}",
        "main{padding:24px 30px}",
        "section{margin-bottom:28px}",
        "h2{margin:0 0 12px 0}",
        "article{background:#fff;border-radius:10px;box-shadow:0 2px 12px rgba(0,0,0,.08);padding:18px;margin-bottom:18px}",
        "img{max-width:100%;border-radius:8px;margin-top:12px}",
        "code{background:#eef;padding:2px 4px;border-radius:4px}",
        "p.meta{font-size:0.95rem;color:#555;margin:4px 0}",
        "footer{padding:18px 30px;background:#eee;color:#333;text-align:center}",
        "</style>",
        "</head>",
        "<body>",
        "<header>",
        f"<h1>{title}</h1>",
        f"<p>{author_description}</p>",
        f"<p><strong>Autor:</strong> {author_name}</p>",
        "</header>",
        "<main>",
    ]

    for group in groups:
        html.append("<section>")
        html.append(f"<h2>{group['title']}</h2>")
        html.append(f"<p>{group['description']}</p>")
        for series in group["series"]:
            html.append("<article>")
            html.append(f"<h3>{series['title']}</h3>")
            html.append(f"<p class=\"meta\"><strong>ID:</strong> {series['id']} | <strong>Año:</strong> {series['year']} | <strong>Estilo:</strong> {series['style']} | <strong>NSFW:</strong> {series['nsfw']}</p>")
            html.append(f"<p>{series['description']}</p>")
            html.append(f"<p class=\"meta\"><strong>Tags:</strong> {', '.join(series['tags'])}</p>")
            for file_url in series["files"]:
                html.append(f"<img src=\"{file_url}\" alt=\"{series['title']}\" />")
            html.append("</article>")
        html.append("</section>")

    html.append("</main>")
    html.append("<footer><p>Sitio generado automáticamente por MiArte Omi.</p></footer>")
    html.append("</body>")
    html.append("</html>")

    with open(os.path.join(WEBSITE_DIR, "index.html"), "w", encoding="utf-8") as handle:
        handle.write("\n".join(html))

def run():
    generate_site()
    root = tk.Tk()
    root.withdraw()
    messagebox.showinfo("Generar sitio", f"El sitio web se generó correctamente en {WEBSITE_DIR}.")

if __name__ == "__main__":
    run()
