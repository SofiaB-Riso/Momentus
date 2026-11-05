from flask import Blueprint, request
from services.propostas.atualizar_proposta_service import AtualizarPropostaService
from services.propostas.comparar_propostas_service import CompararPropostasService
from services.propostas.criar_proposta_service import CriarPropostaService
from services.propostas.remover_proposta_service import RemoverPropostaService
from utils.auth import login_required

from controllers.contexto import obter_caso
from controllers.registro import registrar_controller
from controllers.respostas import ler_json, responder

propostas_controller = Blueprint("propostas_controller", __name__)


class PropostasController:
    @login_required
    def criar(self, evento_id):
        return responder(
            obter_caso(CriarPropostaService).executar(evento_id, ler_json())
        )

    @login_required
    def atualizar(self, evento_id, proposta_id):
        return responder(
            obter_caso(AtualizarPropostaService).executar(
                evento_id, proposta_id, ler_json()
            )
        )

    @login_required
    def remover(self, evento_id, proposta_id):
        return responder(
            obter_caso(RemoverPropostaService).executar(evento_id, proposta_id)
        )

    @login_required
    def comparar(self, evento_id):
        return responder(
            obter_caso(CompararPropostasService).executar(
                evento_id, request.args.to_dict()
            )
        )


registrar_controller(
    propostas_controller,
    PropostasController,
    [
        ["POST", "/eventos/<int:evento_id>/propostas", "criar"],
        ["PUT", "/eventos/<int:evento_id>/propostas/<int:proposta_id>", "atualizar"],
        ["DELETE", "/eventos/<int:evento_id>/propostas/<int:proposta_id>", "remover"],
        ["GET", "/eventos/<int:evento_id>/propostas/comparacao", "comparar"],
        ["GET", "/eventos/<int:evento_id>/propostas", "comparar"],
    ],
)
