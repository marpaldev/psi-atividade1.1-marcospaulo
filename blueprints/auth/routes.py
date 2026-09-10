from flask import request, redirect, url_for, render_template, session
from . import auth_bp
import models

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        for u in models.usuarios:
            if u["nome"] == request.form["nome"] and u["senha"] == request.form["senha"]:
                session["usuario"] = u["nome"]
                return redirect(url_for("index"))
        return render_template("login.html", erro="Credenciais inválidas")
    return render_template("login.html")


@auth_bp.route("/logout")
def logout():
    session.pop("usuario", None)
    return redirect(url_for("index"))