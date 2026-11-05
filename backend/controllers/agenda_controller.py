from flask import Blueprint
from services.agenda.verificar_conflitos_service import VerificarConflitosAgendaService
from utils.auth import login_required

from controllers.contexto import obter_caso
from controllers.registro import registrar_controller
from controllers.respostas import ler_json, responder

agenda_controller = Blueprint("agenda_controller", __name__)


class AgendaController:
    @login_required
    def verificar(self):
        return responder(
            obter_caso(VerificarConflitosAgendaService).executar(ler_json())
        )


registrar_controller(
    agenda_controller, AgendaController, [["POST", "/eventos/conflitos", "verificar"]]
)
