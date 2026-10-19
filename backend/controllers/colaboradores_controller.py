from flask import Blueprint, request
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
from controllers.respostas import responder

colaboradores_controller = Blueprint("colaboradores_controller", __name__)


@colaboradores_controller.get("/colaboracoes/<token>")
def ver_colaboracao(token):
    caso = obter_caso(VerColaboracaoService)
    return responder(caso.executar(token))


@colaboradores_controller.post("/eventos/<int:evento_id>/colaboradores")
@login_required
def adicionar_colaborador(evento_id):
    caso = obter_caso(AdicionarColaboradorService)
    return responder(
        caso.executar(evento_id, dados=request.get_json(silent=True) or {})
    )


@colaboradores_controller.post("/colaboracoes/<token>/responder")
@login_required
def responder_colaboracao(token):
    caso = obter_caso(ResponderColaboracaoService)
    return responder(caso.executar(token, dados=request.get_json(silent=True) or {}))


@colaboradores_controller.put(
    "/eventos/<int:evento_id>/colaboradores/<int:colaborador_id>"
)
@login_required
def atualizar_colaborador(evento_id, colaborador_id):
    caso = obter_caso(AtualizarColaboradorService)
    return responder(
        caso.executar(
            evento_id, colaborador_id, dados=request.get_json(silent=True) or {}
        )
    )


@colaboradores_controller.delete(
    "/eventos/<int:evento_id>/colaboradores/<int:colaborador_id>"
)
@login_required
def remover_colaborador(evento_id, colaborador_id):
    caso = obter_caso(RemoverColaboradorService)
    return responder(caso.executar(evento_id, colaborador_id))
