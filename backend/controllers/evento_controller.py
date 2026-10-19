from flask import Blueprint, request
from services.evento.atualizar_evento_service import AtualizarEventoService
from services.evento.buscar_evento_por_id_service import BuscarEventoPorIdService
from services.evento.buscar_eventos_por_tipo_service import BuscarEventosPorTipoService
from services.evento.criar_evento_service import CriarEventoService
from services.evento.deletar_evento_service import DeletarEventoService
from services.evento.listar_eventos_service import ListarEventosService
from utils.auth import login_required

from controllers.contexto import obter_caso
from controllers.respostas import responder

evento_controller = Blueprint("evento_controller", __name__)


@evento_controller.post("/eventos")
@login_required
def criar_evento():
    caso = obter_caso(CriarEventoService)
    return responder(caso.executar(dados=request.get_json(silent=True) or {}))


@evento_controller.get("/eventos")
@login_required
def listar_eventos():
    caso = obter_caso(ListarEventosService)
    return responder(caso.executar())


@evento_controller.get("/eventos/por-tipo")
@login_required
def buscar_eventos_por_tipo():
    caso = obter_caso(BuscarEventosPorTipoService)
    return responder(caso.executar(params=request.args.to_dict()))


@evento_controller.get("/eventos/<int:evento_id>")
@login_required
def buscar_evento_por_id(evento_id):
    caso = obter_caso(BuscarEventoPorIdService)
    return responder(
        caso.executar(evento_id, dados=request.get_json(silent=True) or {})
    )


@evento_controller.put("/eventos/<int:evento_id>")
@login_required
def atualizar_evento(evento_id):
    caso = obter_caso(AtualizarEventoService)
    return responder(
        caso.executar(evento_id, dados=request.get_json(silent=True) or {})
    )


@evento_controller.delete("/eventos/<int:evento_id>")
@login_required
def deletar_evento(evento_id):
    caso = obter_caso(DeletarEventoService)
    return responder(caso.executar(evento_id))
