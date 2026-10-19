from flask import Blueprint
from services.historico.listar_logs_service import ListarLogsService
from utils.auth import login_required

from controllers.contexto import obter_caso
from controllers.respostas import responder

historico_controller = Blueprint("historico_controller", __name__)


@historico_controller.get("/eventos/<int:evento_id>/logs")
@login_required
def listar_logs(evento_id):
    caso = obter_caso(ListarLogsService)
    return responder(caso.executar(evento_id))
