from flask import Blueprint
from services.colaboradores.adicionar_colaborador_service import (
    AdicionarColaboradorService,
)
from services.colaboradores.atualizar_colaborador_service import (
    AtualizarColaboradorService,
)
from services.colaboradores.remover_colaborador_service import RemoverColaboradorService
from services.colaboradores.responder_colaboracao_service import (
    ResponderColaboracaoService,
)
from services.colaboradores.ver_colaboracao_service import VerColaboracaoService
from utils.auth import login_required

from controllers.contexto import obter_caso
from controllers.registro import registrar_controller
from controllers.respostas import ler_json, responder

colaboradores_controller = Blueprint("colaboradores_controller", __name__)


class ColaboradoresController:
    """Adaptador HTTP do recurso; regras de negócio ficam nos Services."""

    def ver_colaboracao(self, token):
        caso = obter_caso(VerColaboracaoService)
        return responder(caso.executar(token))

    @login_required
    def adicionar_colaborador(self, evento_id):
        caso = obter_caso(AdicionarColaboradorService)
        return responder(caso.executar(evento_id, dados=ler_json()))

    @login_required
    def responder_colaboracao(self, token):
        caso = obter_caso(ResponderColaboracaoService)
        return responder(caso.executar(token, dados=ler_json()))

    @login_required
    def atualizar_colaborador(self, evento_id, colaborador_id):
        caso = obter_caso(AtualizarColaboradorService)
        return responder(caso.executar(evento_id, colaborador_id, dados=ler_json()))

    @login_required
    def remover_colaborador(self, evento_id, colaborador_id):
        caso = obter_caso(RemoverColaboradorService)
        return responder(caso.executar(evento_id, colaborador_id))


registrar_controller(
    colaboradores_controller,
    ColaboradoresController,
    [
        ("GET", "/colaboracoes/<token>", "ver_colaboracao"),
        ("POST", "/eventos/<int:evento_id>/colaboradores", "adicionar_colaborador"),
        ("POST", "/colaboracoes/<token>/responder", "responder_colaboracao"),
        (
            "PUT",
            "/eventos/<int:evento_id>/colaboradores/<int:colaborador_id>",
            "atualizar_colaborador",
        ),
        (
            "DELETE",
            "/eventos/<int:evento_id>/colaboradores/<int:colaborador_id>",
            "remover_colaborador",
        ),
    ],
)
