from flask import Blueprint, request
from services.convidados.adicionar_convidado_service import AdicionarConvidadoService
from services.convidados.assumir_item_rsvp_service import AssumirItemRsvpService
from services.convidados.atualizar_convidado_service import AtualizarConvidadoService
from services.convidados.liberar_item_rsvp_service import LiberarItemRsvpService
from services.convidados.listar_convidados_service import ListarConvidadosService
from services.convidados.remover_convidado_service import RemoverConvidadoService
from services.convidados.responder_rsvp_service import ResponderRsvpService
from services.convidados.ver_rsvp_service import VerRsvpService
from utils.auth import login_required

from controllers.contexto import obter_caso
from controllers.respostas import responder

convidados_controller = Blueprint("convidados_controller", __name__)


@convidados_controller.get("/eventos/<int:evento_id>/convidados")
@login_required
def listar_convidados(evento_id):
    caso = obter_caso(ListarConvidadosService)
    return responder(caso.executar(evento_id))


@convidados_controller.post("/eventos/<int:evento_id>/convidados")
@login_required
def adicionar_convidado(evento_id):
    caso = obter_caso(AdicionarConvidadoService)
    return responder(
        caso.executar(evento_id, dados=request.get_json(silent=True) or {})
    )


@convidados_controller.put("/eventos/<int:evento_id>/convidados/<int:convidado_id>")
@login_required
def atualizar_convidado(evento_id, convidado_id):
    caso = obter_caso(AtualizarConvidadoService)
    return responder(
        caso.executar(
            evento_id, convidado_id, dados=request.get_json(silent=True) or {}
        )
    )


@convidados_controller.delete("/eventos/<int:evento_id>/convidados/<int:convidado_id>")
@login_required
def remover_convidado(evento_id, convidado_id):
    caso = obter_caso(RemoverConvidadoService)
    return responder(caso.executar(evento_id, convidado_id))


@convidados_controller.get("/rsvp/<token>")
def ver_rsvp(token):
    caso = obter_caso(VerRsvpService)
    return responder(caso.executar(token))


@convidados_controller.post("/rsvp/<token>")
def responder_rsvp(token):
    caso = obter_caso(ResponderRsvpService)
    return responder(caso.executar(token, dados=request.get_json(silent=True) or {}))


@convidados_controller.post("/rsvp/<token>/itens/<int:item_id>/assumir")
def assumir_item_rsvp(token, item_id):
    caso = obter_caso(AssumirItemRsvpService)
    return responder(caso.executar(token, item_id))


@convidados_controller.post("/rsvp/<token>/itens/<int:item_id>/liberar")
def liberar_item_rsvp(token, item_id):
    caso = obter_caso(LiberarItemRsvpService)
    return responder(caso.executar(token, item_id))
