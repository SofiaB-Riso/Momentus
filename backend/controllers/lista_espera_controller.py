from flask import Blueprint
from services.lista_espera.configurar_vagas_service import ConfigurarVagasService
from services.lista_espera.consultar_lista_espera_service import (
    ConsultarListaEsperaService,
)
from utils.auth import login_required

from controllers.contexto import obter_caso
from controllers.registro import registrar_controller
from controllers.respostas import ler_json, responder

lista_espera_controller = Blueprint("lista_espera_controller", __name__)


class ListaEsperaController:
    @login_required
    def consultar(self, evento_id):
        return responder(obter_caso(ConsultarListaEsperaService).executar(evento_id))

    @login_required
    def configurar(self, evento_id):
        return responder(
            obter_caso(ConfigurarVagasService).executar(evento_id, ler_json())
        )


registrar_controller(
    lista_espera_controller,
    ListaEsperaController,
    [
        ["GET", "/eventos/<int:evento_id>/lista-espera", "consultar"],
        ["PUT", "/eventos/<int:evento_id>/lista-espera", "configurar"],
    ],
)
