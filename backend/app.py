import os
from datetime import timedelta
from pathlib import Path

from controllers.agenda_controller import agenda_controller
from controllers.auth_controller import auth_controller
from controllers.autorizacoes_controller import autorizacoes_controller
from controllers.catalogo_controller import catalogo_controller
from controllers.colaboradores_controller import colaboradores_controller
from controllers.convidados_controller import convidados_controller
from controllers.cronograma_controller import cronograma_controller
from controllers.evento_controller import evento_controller
from controllers.financeiro_controller import financeiro_controller
from controllers.fornecedor_controller import fornecedor_controller
from controllers.galeria_controller import galeria_controller
from controllers.historico_controller import historico_controller
from controllers.itens_controller import itens_controller
from controllers.lista_espera_controller import lista_espera_controller
from controllers.locais_controller import locais_controller
from controllers.planejamento_controller import planejamento_controller
from controllers.privacidade_controller import privacidade_controller
from controllers.propostas_controller import propostas_controller
from controllers.relatorios_controller import relatorios_controller
from controllers.sistema_controller import SistemaController
from controllers.tarefas_controller import tarefas_controller
from controllers.usuario_controller import usuario_controller
from dotenv import load_dotenv
from flask import Flask
from models import db  # importa também os models relacionais via models/__init__.py

BASE_DIR = Path(__file__).resolve().parent
FRONTEND_DIR = BASE_DIR.parent / "frontend"
UPLOAD_DIR = BASE_DIR / "uploads"


def create_app(test_config=None):
    load_dotenv(BASE_DIR / ".env")

    app = Flask(__name__, instance_path=str(BASE_DIR / "instance"))
    app.config.update(
        SQLALCHEMY_DATABASE_URI=os.getenv("DATABASE_URL", "sqlite:///momentus.db"),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        SQLALCHEMY_ENGINE_OPTIONS={"hide_parameters": True},
        SECRET_KEY=os.getenv("SECRET_KEY", ""),
        APP_ENV=os.getenv("APP_ENV", "development").strip().lower(),
        PERMANENT_SESSION_LIFETIME=timedelta(hours=8),
        SESSION_REFRESH_EACH_REQUEST=False,
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE="Lax",
        MAX_CONTENT_LENGTH=8 * 1024 * 1024,
        MAX_FORM_MEMORY_SIZE=64 * 1024,
        MAX_FORM_PARTS=30,
        UPLOAD_FOLDER=os.getenv("UPLOAD_FOLDER", str(UPLOAD_DIR)),
    )
    for chave in (
        "PUBLIC_BASE_URL",
        "SMTP_HOST",
        "SMTP_FROM",
        "SMTP_USERNAME",
        "SMTP_PASSWORD",
        "PRIVACY_CONTROLLER",
        "PRIVACY_OFFICER",
        "PRIVACY_EMAIL",
        "PRIVACY_PHONE",
    ):
        app.config[chave] = os.getenv(chave, "")
    app.config["SMTP_PORT"] = os.getenv("SMTP_PORT", "587")
    app.config["SMTP_SSL"] = os.getenv("SMTP_SSL", "false").lower() == "true"
    app.config["PRIVACY_DEMO"] = os.getenv("PRIVACY_DEMO", "true").lower() == "true"
    if app.config["PRIVACY_DEMO"]:
        exemplos = {
            "PRIVACY_CONTROLLER": "Sofia Braga Riso",
            "PRIVACY_OFFICER": "Sofie Cirino e Castro",
            "PRIVACY_EMAIL": "momentus@momentus.com",
            "PRIVACY_PHONE": "+55 31 99999-9999",
        }
        for chave, valor in exemplos.items():
            app.config[chave] = app.config[chave] or valor
    if test_config:
        app.config.update(test_config)

    from infrastructure.seguranca import (
        registrar_seguranca,
        segredo_instalacao,
        validar_producao,
    )

    validar_producao(app.config)
    if not app.config["SECRET_KEY"] or app.config["SECRET_KEY"].startswith("troque-"):
        app.config["SECRET_KEY"] = segredo_instalacao(app.instance_path)
    app.config.setdefault("CSRF_ENABLED", not app.testing)
    app.config.setdefault("RATE_LIMIT_ENABLED", not app.testing)
    if os.getenv("TRUST_PROXY_HEADERS", "false").lower() == "true":
        from werkzeug.middleware.proxy_fix import ProxyFix

        app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1)
    registrar_seguranca(app)

    db.init_app(app)

    from application.composicao import Composicao
    from controllers.respostas import registrar_erros

    app.extensions["momentus"] = Composicao(app.config)
    registrar_erros(app)
    app.register_blueprint(planejamento_controller)
    app.register_blueprint(auth_controller)
    app.register_blueprint(agenda_controller)
    app.register_blueprint(propostas_controller)
    app.register_blueprint(cronograma_controller)
    app.register_blueprint(lista_espera_controller)
    app.register_blueprint(autorizacoes_controller)
    app.register_blueprint(privacidade_controller)
    app.register_blueprint(catalogo_controller)
    app.register_blueprint(evento_controller)
    app.register_blueprint(fornecedor_controller)
    app.register_blueprint(usuario_controller)
    app.register_blueprint(convidados_controller)
    app.register_blueprint(colaboradores_controller)
    app.register_blueprint(itens_controller)
    app.register_blueprint(tarefas_controller)
    app.register_blueprint(financeiro_controller)
    app.register_blueprint(galeria_controller)
    app.register_blueprint(historico_controller)
    app.register_blueprint(relatorios_controller)
    app.register_blueprint(locais_controller)

    @app.cli.command("gerar-lembretes")
    def gerar_lembretes_cli():
        from services.lembretes_service import GerarLembretesService

        GerarLembretesService().executar(transacao=app.extensions["momentus"].transacao)
        print("Lembretes internos atualizados.")

    SistemaController(FRONTEND_DIR).registrar(app)

    with app.app_context():
        db.create_all()

    return app


app = create_app()


if __name__ == "__main__":
    debug = (
        app.config["APP_ENV"] != "production"
        and os.getenv("FLASK_DEBUG", "False").lower() == "true"
    )
    app.run(debug=debug, host="0.0.0.0", port=int(os.getenv("PORT", "5000")))
