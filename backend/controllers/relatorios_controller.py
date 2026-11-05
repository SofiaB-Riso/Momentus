from flask import Blueprint, current_app
from utils.auth import login_required, usuario_atual

from controllers.registro import registrar_controller
from controllers.respostas import responder

relatorios_controller = Blueprint("relatorios_controller", __name__)


class RelatoriosController:
    """Adaptador HTTP do recurso; regras de negócio ficam nos Services."""

    @login_required
    def relatorio_pdf(self, evento_id):
        caso = current_app.extensions["momentus"].relatorio("pdf", usuario_atual().id)
        return responder(caso.executar(evento_id))

    @login_required
    def relatorio_xlsx(self, evento_id):
        caso = current_app.extensions["momentus"].relatorio("xlsx", usuario_atual().id)
        return responder(caso.executar(evento_id))


registrar_controller(
    relatorios_controller,
    RelatoriosController,
    [
        ("GET", "/eventos/<int:evento_id>/relatorio.pdf", "relatorio_pdf"),
        ("GET", "/eventos/<int:evento_id>/relatorio.xlsx", "relatorio_xlsx"),
    ],
)
