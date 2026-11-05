from flask import Blueprint
from services.historico.listar_logs_service import ListarLogsService
from utils.auth import login_required

from controllers.contexto import obter_caso
from controllers.registro import registrar_controller
from controllers.respostas import responder

historico_controller = Blueprint("historico_controller", __name__)


class HistoricoController:
    """Adaptador HTTP do recurso; regras de negócio ficam nos Services."""

    @login_required
    def listar_logs(self, evento_id):
        caso = obter_caso(ListarLogsService)
        return responder(caso.executar(evento_id))


registrar_controller(
    historico_controller,
    HistoricoController,
    [
        ("GET", "/eventos/<int:evento_id>/logs", "listar_logs"),
    ],
)
