from flask import Blueprint
from services.cronograma.gerar_cronograma_service import GerarCronogramaService
from utils.auth import login_required

from controllers.contexto import obter_caso
from controllers.registro import registrar_controller
from controllers.respostas import responder

cronograma_controller = Blueprint("cronograma_controller", __name__)


class CronogramaController:
    @login_required
    def gerar(self, evento_id):
        return responder(obter_caso(GerarCronogramaService).executar(evento_id))


registrar_controller(
    cronograma_controller,
    CronogramaController,
    [["POST", "/eventos/<int:evento_id>/cronograma", "gerar"]],
)
