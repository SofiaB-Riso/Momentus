import os
from dotenv import load_dotenv
from flask import Flask, jsonify
from flask_cors import CORS

from models.database import db
from controllers.evento_controller import evento_controller


def create_app():
    load_dotenv()

    app = Flask(__name__)
    CORS(app)

    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL", "sqlite:///evento.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    app.register_blueprint(evento_controller)

    @app.get("/")
    def home():
        return jsonify({
            "mensagem": "API Flask + SQLAlchemy funcionando.",
            "rotas": {
                "listar_eventos": "GET /eventos",
                "buscar_evento": "GET /eventos/<id>",
                "buscar_por_evento_tipo": "GET /eventos/por-tipo?tipo_evento=Casamento",
                "criar_evento": "POST /eventos",
                "atualizar_evento": "PUT /eventos/<id>",
                "deletar_evento": "DELETE /eventos/<id>",
            }
        })

    with app.app_context():
        # Cria as tabelas automaticamente para facilitar os testes em sala.
        # Em produção, o ideal é usar migrations.
        db.create_all()

    return app


app = create_app()


if __name__ == "__main__":
    debug = os.getenv("FLASK_DEBUG", "True") == "True"
    app.run(debug=debug, host="0.0.0.0", port=5000)
