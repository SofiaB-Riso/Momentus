"""Transporte dos arquivos da interface e informações de execução do servidor."""

from pathlib import Path

from flask import current_app, jsonify, send_from_directory
from services.conta.acessar_arquivo_service import AcessarArquivoService
from utils.auth import login_required

from controllers.contexto import obter_caso


class SistemaController:
    def csrf(self):
        from infrastructure.seguranca import token_csrf

        return jsonify(token=token_csrf(criar=True))

    def __init__(self, frontend_dir):
        self.frontend_dir = frontend_dir

    def api_status(self):
        return jsonify(
            {
                "nome": "Momentus",
                "status": "online",
                "autenticacao": "sessão HttpOnly",
                "banco": current_app.config["SQLALCHEMY_DATABASE_URI"].split(":", 1)[0],
            }
        )

    @login_required
    def uploads(self, filename):
        obter_caso(AcessarArquivoService).executar(filename)
        pasta = Path(current_app.config["UPLOAD_FOLDER"])
        pasta.mkdir(parents=True, exist_ok=True)
        resposta = send_from_directory(pasta, filename)
        resposta.headers["Cache-Control"] = "private, no-store"
        resposta.headers["X-Content-Type-Options"] = "nosniff"
        return resposta

    def frontend_home(self):
        return send_from_directory(self.frontend_dir, "index.html")

    def frontend_files(self, filename):
        caminho = self.frontend_dir / filename
        if caminho.is_file():
            return send_from_directory(self.frontend_dir, filename)
        return jsonify({"erro": "Página ou recurso não encontrado."}), 404

    def registrar(self, app):
        for caminho, acao in (
            ("/auth/csrf", "csrf"),
            ("/api/status", "api_status"),
            ("/uploads/<path:filename>", "uploads"),
            ("/", "frontend_home"),
            ("/<path:filename>", "frontend_files"),
        ):
            app.add_url_rule(caminho, endpoint=acao, view_func=getattr(self, acao))
