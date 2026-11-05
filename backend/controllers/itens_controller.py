from flask import Blueprint
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
from controllers.registro import registrar_controller
from controllers.respostas import ler_json, responder

itens_controller = Blueprint("itens_controller", __name__)


class ItensController:
    """Adaptador HTTP do recurso; regras de negócio ficam nos Services."""

    @login_required
    def criar_item_compartilhado(self, evento_id):
        caso = obter_caso(CriarItemCompartilhadoService)
        return responder(caso.executar(evento_id, dados=ler_json()))

    @login_required
    def atualizar_item_compartilhado(self, evento_id, item_id):
        caso = obter_caso(AtualizarItemCompartilhadoService)
        return responder(caso.executar(evento_id, item_id, dados=ler_json()))

    @login_required
    def remover_item_compartilhado(self, evento_id, item_id):
        caso = obter_caso(RemoverItemCompartilhadoService)
        return responder(caso.executar(evento_id, item_id))

    @login_required
    def adicionar_item_evento(self, evento_id):
        caso = obter_caso(AdicionarItemEventoService)
        return responder(caso.executar(evento_id, dados=ler_json()))

    @login_required
    def remover_item_evento(self, evento_id, item_id):
        caso = obter_caso(RemoverItemEventoService)
        return responder(caso.executar(evento_id, item_id))


registrar_controller(
    itens_controller,
    ItensController,
    [
        (
            "POST",
            "/eventos/<int:evento_id>/itens-compartilhados",
            "criar_item_compartilhado",
        ),
        (
            "PUT",
            "/eventos/<int:evento_id>/itens-compartilhados/<int:item_id>",
            "atualizar_item_compartilhado",
        ),
        (
            "DELETE",
            "/eventos/<int:evento_id>/itens-compartilhados/<int:item_id>",
            "remover_item_compartilhado",
        ),
        ("POST", "/eventos/<int:evento_id>/itens", "adicionar_item_evento"),
        (
            "DELETE",
            "/eventos/<int:evento_id>/itens/<int:item_id>",
            "remover_item_evento",
        ),
    ],
)
