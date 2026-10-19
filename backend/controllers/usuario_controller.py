from flask import Blueprint, request
from services.usuario.alternar_favorito_service import AlternarFavoritoService
from services.usuario.listar_favoritos_service import ListarFavoritosService
from services.usuario.listar_notificacoes_service import ListarNotificacoesService
from services.usuario.marcar_notificacoes_lidas_service import (
    MarcarNotificacoesLidasService,
)
from utils.auth import login_required

from controllers.contexto import obter_caso
from controllers.respostas import responder

usuario_controller = Blueprint("usuario_controller", __name__)


@usuario_controller.get("/notificacoes")
@login_required
def listar_notificacoes():
    caso = obter_caso(ListarNotificacoesService)
    return responder(caso.executar())


@usuario_controller.put("/notificacoes/lidas")
@login_required
def marcar_notificacoes_lidas():
    caso = obter_caso(MarcarNotificacoesLidasService)
    return responder(caso.executar())


@usuario_controller.get("/favoritos")
@login_required
def listar_favoritos():
    caso = obter_caso(ListarFavoritosService)
    return responder(caso.executar())


@usuario_controller.post("/favoritos")
@login_required
def alternar_favorito():
    caso = obter_caso(AlternarFavoritoService)
    return responder(caso.executar(dados=request.get_json(silent=True) or {}))
