from flask import Blueprint
from services.conta.responder_autorizacao_service import (
    ResponderAutorizacaoResponsavelService,
)
from services.conta.ver_link_responsavel_service import VerLinkResponsavelService

from controllers.contexto import obter_caso
from controllers.registro import registrar_controller
from controllers.respostas import ler_json, responder

autorizacoes_controller = Blueprint("autorizacoes_controller", __name__)


class AutorizacoesController:
    def consultar(self):
        return responder(obter_caso(VerLinkResponsavelService).executar(ler_json()))

    def responder(self):
        return responder(
            obter_caso(ResponderAutorizacaoResponsavelService).executar(ler_json())
        )


registrar_controller(
    autorizacoes_controller,
    AutorizacoesController,
    [
        ("POST", "/autorizacoes/consultar", "consultar"),
        ("POST", "/autorizacoes/responder", "responder"),
    ],
)
