from flask import Flask, render_template, request
from pathlib import Path
from parser import parse_cronograma

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    # listar archivos .md o .txt en la carpeta user_files
    folder = Path("user_files")
    archivos = [f.name for f in folder.glob("*.md")] + [f.name for f in folder.glob("*.txt")]

    # archivo seleccionado (por defecto, el primero de la lista)
    archivo_sel = request.form.get("archivo", archivos[0] if archivos else None)

    # parsear el archivo seleccionado
    data, titulos = parse_cronograma(folder / archivo_sel)

    return render_template(
        "index.html",
        archivos=archivos,
        archivo_sel=archivo_sel,
        data=data,
        titulos=titulos
    )


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=7988)
