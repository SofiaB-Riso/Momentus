from flask import Blueprint, request
from services.locais.buscar_locais_service import BuscarLocaisService
from services.locais.recomendar_fornecedores_service import (
    RecomendarFornecedoresService,
)
from services.locais.remover_local_service import RemoverLocalService
from services.locais.salvar_local_service import SalvarLocalService
from utils.auth import login_required

from controllers.contexto import obter_caso
from controllers.registro import registrar_controller
from controllers.respostas import ler_json, responder

locais_controller = Blueprint("locais_controller", __name__)


class LocaisController:
    """Adaptador HTTP do recurso; regras de negócio ficam nos Services."""

    @login_required
    def recomendar_fornecedores(self, evento_id):
        return responder(
            obter_caso(RecomendarFornecedoresService).executar(
                evento_id, params=request.args.to_dict()
            )
        )

    @login_required
    def buscar_locais(self, evento_id):
        return responder(
            obter_caso(BuscarLocaisService).executar(
                evento_id, params=request.args.to_dict()
            )
        )

    @login_required
    def salvar_local(self, evento_id):
        return responder(
            obter_caso(SalvarLocalService).executar(evento_id, dados=ler_json())
        )

    @login_required
    def remover_local(self, evento_id, local_id):
        return responder(obter_caso(RemoverLocalService).executar(evento_id, local_id))


registrar_controller(
    locais_controller,
    LocaisController,
    [
        ("GET", "/eventos/<int:evento_id>/recomendacoes", "recomendar_fornecedores"),
        ("GET", "/eventos/<int:evento_id>/locais", "buscar_locais"),
        ("POST", "/eventos/<int:evento_id>/locais", "salvar_local"),
        ("DELETE", "/eventos/<int:evento_id>/locais/<int:local_id>", "remover_local"),
    ],
)
