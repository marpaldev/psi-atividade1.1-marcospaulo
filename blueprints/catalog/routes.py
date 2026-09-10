from flask import render_template, request, url_for, redirect, session
import models
from . import catalog_bp

@catalog_bp.route("/")
def index():
    q = request.args.get("q", "")
    return render_template("index.html", livros=models.buscar_livros(q), q=q)

@catalog_bp.route("/livro/<int:livro_id>")
def ver_livro(livro_id):
    livro = models.buscar_livro(livro_id)
    if livro is None:
        return "Livro não encontrado", 404
    return render_template("livro.html", livro=livro,
                           resenhas=models.resenhas_do_livro(livro_id))


@catalog_bp.route("/livro/<int:livro_id>/resenhar", methods=["POST"])
def resenhar(livro_id):
    if "usuario" not in session:
        return redirect(url_for("login"))
    if models.buscar_livro(livro_id):
        models.resenhas.append({
            "id": models.proximo_id_resenha,
            "livro_id": livro_id,
            "usuario": session["usuario"],
            "texto": request.form["texto"],
            "nota": int(request.form["nota"]),
        })
        models.proximo_id_resenha += 1
    return redirect(url_for("ver_livro", livro_id=livro_id))