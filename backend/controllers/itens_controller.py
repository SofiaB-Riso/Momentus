from flask import Blueprint, request
from services.itens.adicionar_item_evento_service import AdicionarItemEventoService
from services.itens.atualizar_item_compartilhado_service import (
    AtualizarItemCompartilhadoService,
)
from services.itens.criar_item_compartilhado_service import (
    CriarItemCompartilhadoService,
)
from services.itens.remover_item_compartilhado_service import (
    RemoverItemCompartilhadoService,
)
from services.itens.remover_item_evento_service import RemoverItemEventoService
from utils.auth import login_required

from controllers.contexto import obter_caso
from controllers.respostas import responder

itens_controller = Blueprint("itens_controller", __name__)


@itens_controller.post("/eventos/<int:evento_id>/itens-compartilhados")
@login_required
def criar_item_compartilhado(evento_id):
    caso = obter_caso(CriarItemCompartilhadoService)
    return responder(
        caso.executar(evento_id, dados=request.get_json(silent=True) or {})
    )


@itens_controller.put("/eventos/<int:evento_id>/itens-compartilhados/<int:item_id>")
@login_required
def atualizar_item_compartilhado(evento_id, item_id):
    caso = obter_caso(AtualizarItemCompartilhadoService)
    return responder(
        caso.executar(evento_id, item_id, dados=request.get_json(silent=True) or {})
    )


@itens_controller.delete("/eventos/<int:evento_id>/itens-compartilhados/<int:item_id>")
@login_required
def remover_item_compartilhado(evento_id, item_id):
    caso = obter_caso(RemoverItemCompartilhadoService)
    return responder(caso.executar(evento_id, item_id))


@itens_controller.post("/eventos/<int:evento_id>/itens")
@login_required
def adicionar_item_evento(evento_id):
    caso = obter_caso(AdicionarItemEventoService)
    return responder(
        caso.executar(evento_id, dados=request.get_json(silent=True) or {})
    )


@itens_controller.delete("/eventos/<int:evento_id>/itens/<int:item_id>")
@login_required
def remover_item_evento(evento_id, item_id):
    caso = obter_caso(RemoverItemEventoService)
    return responder(caso.executar(evento_id, item_id))
