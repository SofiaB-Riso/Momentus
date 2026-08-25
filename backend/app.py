import os
from pathlib import Path

from dotenv import load_dotenv
from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS

from controllers.auth_controller import auth_controller
from controllers.catalogo_controller import catalogo_controller
from controllers.evento_controller import evento_controller
from controllers.evento_detalhes_controller import evento_detalhes_controller
from controllers.fornecedor_controller import fornecedor_controller
from controllers.usuario_controller import usuario_controller
from models import db  # importa também os models relacionais via models/__init__.py


BASE_DIR = Path(__file__).resolve().parent
FRONTEND_DIR = BASE_DIR.parent / "frontend"
UPLOAD_DIR = BASE_DIR / "uploads"


def create_app(test_config=None):
    load_dotenv()

    app = Flask(__name__)
    app.config.update(
        SQLALCHEMY_DATABASE_URI=os.getenv("DATABASE_URL", "sqlite:///momentus.db"),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        SECRET_KEY=os.getenv("SECRET_KEY", "dev-momentus-troque-em-producao"),
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE="Lax",
        MAX_CONTENT_LENGTH=8 * 1024 * 1024,
        UPLOAD_FOLDER=str(UPLOAD_DIR),
    )
    if test_config:
        app.config.update(test_config)

    # Mantido para facilitar desenvolvimento; a aplicação normal roda no mesmo
    # host do Flask e usa cookie HttpOnly de sessão, sem token no localStorage.
    CORS(app, supports_credentials=True, origins=["http://127.0.0.1:5000", "http://localhost:5000"])

    db.init_app(app)

    app.register_blueprint(auth_controller)
    app.register_blueprint(catalogo_controller)
    app.register_blueprint(evento_controller)
    app.register_blueprint(evento_detalhes_controller)
    app.register_blueprint(fornecedor_controller)
    app.register_blueprint(usuario_controller)

    @app.get("/api/status")
    def api_status():
        return jsonify({
            "nome": "Momentus",
            "status": "online",
            "autenticacao": "sessão HttpOnly",
            "banco": app.config["SQLALCHEMY_DATABASE_URI"].split(":", 1)[0],
        })

    @app.get("/uploads/<path:filename>")
    def uploads(filename):
        UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
        return send_from_directory(UPLOAD_DIR, filename)

    @app.get("/")
    def frontend_home():
        return send_from_directory(FRONTEND_DIR, "index.html")

    @app.get("/<path:filename>")
    def frontend_files(filename):
        caminho = FRONTEND_DIR / filename
        if caminho.is_file():
            return send_from_directory(FRONTEND_DIR, filename)
        return jsonify({"erro": "Página ou recurso não encontrado."}), 404

    with app.app_context():
        db.create_all()

    return app


app = create_app()


if __name__ == "__main__":
    debug = os.getenv("FLASK_DEBUG", "True").lower() == "true"
    app.run(debug=debug, host="0.0.0.0", port=int(os.getenv("PORT", "5000")))
