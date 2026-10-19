from flask import Blueprint, request
from services.locais.buscar_locais_service import BuscarLocaisService
from services.locais.recomendar_fornecedores_service import (
    RecomendarFornecedoresService,
)
from services.locais.remover_local_service import RemoverLocalService
from services.locais.salvar_local_service import SalvarLocalService
from utils.auth import login_required

from controllers.contexto import obter_caso
from controllers.respostas import responder

locais_controller = Blueprint("locais_controller", __name__)


@locais_controller.get("/eventos/<int:evento_id>/recomendacoes")
@login_required
def recomendar_fornecedores(evento_id):
    return responder(
        obter_caso(RecomendarFornecedoresService).executar(
            evento_id, params=request.args.to_dict()
        )
    )


@locais_controller.get("/eventos/<int:evento_id>/locais")
@login_required
def buscar_locais(evento_id):
    return responder(
        obter_caso(BuscarLocaisService).executar(
            evento_id, params=request.args.to_dict()
        )
    )


@locais_controller.post("/eventos/<int:evento_id>/locais")
@login_required
def salvar_local(evento_id):
    return responder(
        obter_caso(SalvarLocalService).executar(
            evento_id, dados=request.get_json(silent=True) or {}
        )
    )


@locais_controller.delete("/eventos/<int:evento_id>/locais/<int:local_id>")
@login_required
def remover_local(evento_id, local_id):
    return responder(obter_caso(RemoverLocalService).executar(evento_id, local_id))
