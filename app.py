from flask import Flask, render_template, request
from blueprints.auth import auth_bp
from blueprints.catalog import catalog_bp
import models

app = Flask(__name__)
app.secret_key = "chave-secreta"

app.register_blueprint(auth_bp)
app.register_blueprint(catalog_bp)

if __name__ == "__main__":
    app.run(debug=True)
