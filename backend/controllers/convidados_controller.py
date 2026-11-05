from flask import Blueprint
from services.convidados.adicionar_convidado_service import AdicionarConvidadoService
from services.convidados.assumir_item_rsvp_service import AssumirItemRsvpService
from services.convidados.atualizar_convidado_service import AtualizarConvidadoService
from services.convidados.gerar_autorizacao_service import (
    GerarLinkResponsavelConvidadoService,
)
from services.convidados.liberar_item_rsvp_service import LiberarItemRsvpService
from services.convidados.listar_convidados_service import ListarConvidadosService
from services.convidados.remover_convidado_service import RemoverConvidadoService
from services.convidados.responder_rsvp_service import ResponderRsvpService
from services.convidados.ver_rsvp_service import VerRsvpService
from utils.auth import login_required

from controllers.contexto import obter_caso
from controllers.registro import registrar_controller
from controllers.respostas import ler_json, responder

convidados_controller = Blueprint("convidados_controller", __name__)


class ConvidadosController:
    """Adaptador HTTP do recurso; regras de negócio ficam nos Services."""

    def gerar_link_responsavel(self, token):
        return responder(
            obter_caso(GerarLinkResponsavelConvidadoService).executar(token)
        )

    @login_required
    def listar_convidados(self, evento_id):
        caso = obter_caso(ListarConvidadosService)
        return responder(caso.executar(evento_id))

    @login_required
    def adicionar_convidado(self, evento_id):
        caso = obter_caso(AdicionarConvidadoService)
        return responder(caso.executar(evento_id, dados=ler_json()))

    @login_required
    def atualizar_convidado(self, evento_id, convidado_id):
        caso = obter_caso(AtualizarConvidadoService)
        return responder(caso.executar(evento_id, convidado_id, dados=ler_json()))

    @login_required
    def remover_convidado(self, evento_id, convidado_id):
        caso = obter_caso(RemoverConvidadoService)
        return responder(caso.executar(evento_id, convidado_id))

    def ver_rsvp(self, token):
        caso = obter_caso(VerRsvpService)
        return responder(caso.executar(token))

    def responder_rsvp(self, token):
        caso = obter_caso(ResponderRsvpService)
        return responder(caso.executar(token, dados=ler_json()))

    def assumir_item_rsvp(self, token, item_id):
        caso = obter_caso(AssumirItemRsvpService)
        return responder(caso.executar(token, item_id))

    def liberar_item_rsvp(self, token, item_id):
        caso = obter_caso(LiberarItemRsvpService)
        return responder(caso.executar(token, item_id))


registrar_controller(
    convidados_controller,
    ConvidadosController,
    [
        ("POST", "/rsvp/<token>/responsavel", "gerar_link_responsavel"),
        ("GET", "/eventos/<int:evento_id>/convidados", "listar_convidados"),
        ("POST", "/eventos/<int:evento_id>/convidados", "adicionar_convidado"),
        (
            "PUT",
            "/eventos/<int:evento_id>/convidados/<int:convidado_id>",
            "atualizar_convidado",
        ),
        (
            "DELETE",
            "/eventos/<int:evento_id>/convidados/<int:convidado_id>",
            "remover_convidado",
        ),
        ("GET", "/rsvp/<token>", "ver_rsvp"),
        ("POST", "/rsvp/<token>", "responder_rsvp"),
        ("POST", "/rsvp/<token>/itens/<int:item_id>/assumir", "assumir_item_rsvp"),
        ("POST", "/rsvp/<token>/itens/<int:item_id>/liberar", "liberar_item_rsvp"),
    ],
)
