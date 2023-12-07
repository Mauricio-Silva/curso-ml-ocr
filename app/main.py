from flask import Flask, render_template, request, abort
from werkzeug.exceptions import InternalServerError
from get_film_opinion import GetFilmOpinion
from common import HOST, PORT, TOKEN
from get_qrcode import GetQrCode
from flask_cors import CORS
# cSpell:ignoreRegExp string


app = Flask(__name__)
GetFilmOpinion.load_ml_model()
CORS(app)


@app.get("/")
def render_index():
    return render_template("index.html")


@app.post("/upload_image")
def processing():
    token = request.form.get("token")

    if not token or token != TOKEN:
        abort(500, "Falha de Autorização")

    buffer_file = request.files.get("photo")

    if not buffer_file:
        abort(500, "Arquivo de imagem não encontrado")

    try:
        opinion = GetFilmOpinion().handle(buffer_file)
        return render_template("success.html", message=opinion)
    except ValueError:
        abort(500, "Erro no processamento de dados")


@app.errorhandler(400)
def bad_request(_):
    description = "Erro inesperado no processamento"
    return render_template("error.html", message=description)


@app.errorhandler(500)
def internal_error(error: InternalServerError):
    return render_template("error.html", message=error.description)


@app.get("/qrcode")
def render_qrcode():
    return render_template("qrcode.html", path=GetQrCode.PATH.removeprefix("app/"))


GetQrCode.render()
print("\033[33mApp Running 🚀\033[m\n")
app.run(host=HOST, port=PORT)
