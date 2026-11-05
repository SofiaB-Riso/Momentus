from flask import Blueprint
from services.usuario.alternar_favorito_service import AlternarFavoritoService
from services.usuario.listar_favoritos_service import ListarFavoritosService
from services.usuario.listar_notificacoes_service import ListarNotificacoesService
from services.usuario.marcar_notificacoes_lidas_service import (
    MarcarNotificacoesLidasService,
)
from utils.auth import login_required

from controllers.contexto import obter_caso
from controllers.registro import registrar_controller
from controllers.respostas import ler_json, responder

usuario_controller = Blueprint("usuario_controller", __name__)


class UsuarioController:
    """Adaptador HTTP do recurso; regras de negócio ficam nos Services."""

    @login_required
    def listar_notificacoes(self):
        caso = obter_caso(ListarNotificacoesService)
        return responder(caso.executar())

    @login_required
    def marcar_notificacoes_lidas(self):
        caso = obter_caso(MarcarNotificacoesLidasService)
        return responder(caso.executar())

    @login_required
    def listar_favoritos(self):
        caso = obter_caso(ListarFavoritosService)
        return responder(caso.executar())

    @login_required
    def alternar_favorito(self):
        caso = obter_caso(AlternarFavoritoService)
        return responder(caso.executar(dados=ler_json()))


registrar_controller(
    usuario_controller,
    UsuarioController,
    [
        ("GET", "/notificacoes", "listar_notificacoes"),
        ("PUT", "/notificacoes/lidas", "marcar_notificacoes_lidas"),
        ("GET", "/favoritos", "listar_favoritos"),
        ("POST", "/favoritos", "alternar_favorito"),
    ],
)
