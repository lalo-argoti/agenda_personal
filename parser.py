# app.py
import os
from flask import Flask, render_template, request
from pathlib import Path

app = Flask(__name__)

def parse_cronograma(md_file):
    data = []
    buffer = []
    current_section = None
    titulos = []  # lista de todos los títulos nivel 1 (# ...)

    with open(md_file, "r", encoding="utf-8") as f:
        lines = f.readlines()

    for line in lines:
        if line.startswith("# "):  
            titulos.append(line[2:].strip())

        elif line.startswith("## "):
            if current_section:
                data.append({
                    "title": current_section,
                    "content": "".join(buffer).strip()
                })
                buffer = []
            current_section = line[3:].strip()
        else:
            buffer.append(line)

    if current_section:
        data.append({
            "title": current_section,
            "content": "".join(buffer).strip()
        })

    return data, titulos


@app.route("/", methods=["GET", "POST"])
def index():
    folder = Path("user_files")
    archivos = [f.name for f in folder.glob("*.md")]

    archivo_sel = request.form.get("archivo", archivos[0] if archivos else None)
    titulos, secciones = parse_cronograma(folder / archivo_sel) if archivo_sel else ([], [])

    titulo_sel = request.form.get("titulo", titulos[0] if titulos else None)

    return render_template(
        "index.html",
        archivos=archivos,
        archivo_sel=archivo_sel,
        titulos=titulos,
        titulo_sel=titulo_sel,
        secciones=secciones
    )

if __name__ == "__main__":
    app.run(debug=True)
