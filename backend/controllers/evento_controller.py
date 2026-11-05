from flask import Blueprint, request
from services.evento.atualizar_evento_service import AtualizarEventoService
from services.evento.buscar_evento_por_id_service import BuscarEventoPorIdService
from services.evento.buscar_eventos_por_tipo_service import BuscarEventosPorTipoService
from services.evento.criar_evento_service import CriarEventoService
from services.evento.deletar_evento_service import DeletarEventoService
from services.evento.listar_eventos_service import ListarEventosService
from utils.auth import login_required

from controllers.contexto import obter_caso
from controllers.registro import registrar_controller
from controllers.respostas import ler_json, responder

evento_controller = Blueprint("evento_controller", __name__)


class EventoController:
    """Adaptador HTTP do recurso; regras de negócio ficam nos Services."""

    @login_required
    def criar_evento(self):
        caso = obter_caso(CriarEventoService)
        return responder(caso.executar(dados=ler_json()))

    @login_required
    def listar_eventos(self):
        caso = obter_caso(ListarEventosService)
        return responder(caso.executar())

    @login_required
    def buscar_eventos_por_tipo(self):
        caso = obter_caso(BuscarEventosPorTipoService)
        return responder(caso.executar(params=request.args.to_dict()))

    @login_required
    def buscar_evento_por_id(self, evento_id):
        caso = obter_caso(BuscarEventoPorIdService)
        return responder(caso.executar(evento_id, dados=ler_json()))

    @login_required
    def atualizar_evento(self, evento_id):
        caso = obter_caso(AtualizarEventoService)
        return responder(caso.executar(evento_id, dados=ler_json()))

    @login_required
    def deletar_evento(self, evento_id):
        caso = obter_caso(DeletarEventoService)
        return responder(caso.executar(evento_id))


registrar_controller(
    evento_controller,
    EventoController,
    [
        ("POST", "/eventos", "criar_evento"),
        ("GET", "/eventos", "listar_eventos"),
        ("GET", "/eventos/por-tipo", "buscar_eventos_por_tipo"),
        ("GET", "/eventos/<int:evento_id>", "buscar_evento_por_id"),
        ("PUT", "/eventos/<int:evento_id>", "atualizar_evento"),
        ("DELETE", "/eventos/<int:evento_id>", "deletar_evento"),
    ],
)
