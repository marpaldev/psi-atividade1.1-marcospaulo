from flask import Flask, render_template, request, redirect, url_for, session
import models

app = Flask(__name__)
app.secret_key = "chave-secreta"


@app.route("/")
def index():
    q = request.args.get("q", "")
    return render_template("index.html", livros=models.buscar_livros(q), q=q)


@app.route("/livro/<int:livro_id>")
def ver_livro(livro_id):
    livro = models.buscar_livro(livro_id)
    if livro is None:
        return "Livro não encontrado", 404
    return render_template("livro.html", livro=livro,
                           resenhas=models.resenhas_do_livro(livro_id))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        for u in models.usuarios:
            if u["nome"] == request.form["nome"] and u["senha"] == request.form["senha"]:
                session["usuario"] = u["nome"]
                return redirect(url_for("index"))
        return render_template("login.html", erro="Credenciais inválidas")
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.pop("usuario", None)
    return redirect(url_for("index"))


@app.route("/livro/<int:livro_id>/resenhar", methods=["POST"])
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


if __name__ == "__main__":
    app.run(debug=True)
