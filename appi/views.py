from django.shortcuts import render
import os


def home(request):
    # Importaciones pesadas solo cuando se solicita la vista (evita cargarlas en el arranque)
    try:
        import nbformat
    except Exception:
        nbformat = None

    # Ruta del notebook (ajusta el nombre/ubicación si es necesario)
    notebook_path = os.path.join(os.path.dirname(__file__), "notebooks", "analisis.ipynb")

    # Si la ruta no existe, intentar buscar cualquier .ipynb en el proyecto
    if not os.path.exists(notebook_path):
        # Buscar en el directorio base del proyecto
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        found = None
        for root, _, files in os.walk(base_dir):
            for fname in files:
                if fname.lower().endswith('.ipynb'):
                    found = os.path.join(root, fname)
                    break
            if found:
                break
        if found:
            notebook_path = found

    # Intentar cargar el archivo .ipynb; si no existe, usar notebook vacío
    if not notebook_path or not os.path.exists(notebook_path) or nbformat is None:
        notebook_node = {"cells": []}
    else:
        with open(notebook_path, "r", encoding="utf-8") as f:
            notebook_node = nbformat.read(f, as_version=4)

    # Construir lista de gráficas con título y descripción (si hay markdown antes del código)
    graficas = []
    last_markdown = None

    for cell in notebook_node.get("cells", []):
        if cell.get("cell_type") == "markdown":
            # Guardar el último markdown para usarlo como título/descripcion de la próxima gráfica
            src = cell.get("source", "")
            # source puede ser lista o string
            if isinstance(src, list):
                src = "".join(src)
            last_markdown = src.strip()

        elif cell.get("cell_type") == "code":
            for output in cell.get("outputs", []):
                if output.get("output_type") in ("display_data", "execute_result"):
                    data = output.get("data", {})
                    if "image/png" in data:
                        image_b64 = data["image/png"]
                        title = "Gráfica"
                        descripcion = ""
                        if last_markdown:
                            # Separar primera línea como título y el resto como descripción
                            lines = [ln for ln in last_markdown.splitlines() if ln.strip()]
                            if lines:
                                title = lines[0]
                                descripcion = "\n".join(lines[1:])
                        graficas.append({
                            "titulo": title,
                            "descripcion": descripcion,
                            "imagen": image_b64,
                        })
                        # Resetear para evitar reasignar la misma markdown a múltiples salidas
                        last_markdown = None

    return render(request, "home.html", {"graficas": graficas})
