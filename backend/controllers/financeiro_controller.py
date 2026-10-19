from flask import Blueprint, request
from services.financeiro.adicionar_despesa_service import AdicionarDespesaService
from services.financeiro.definir_rateio_service import DefinirRateioService
from services.financeiro.enviar_comprovante_service import EnviarComprovanteService
from services.financeiro.listar_despesas_service import ListarDespesasService
from services.financeiro.remover_despesa_service import RemoverDespesaService
from services.financeiro.resumo_evento_service import ResumoEventoService
from utils.auth import login_required

from controllers.contexto import obter_caso
from controllers.respostas import responder

financeiro_controller = Blueprint("financeiro_controller", __name__)


@financeiro_controller.get("/eventos/<int:evento_id>/despesas")
@login_required
def listar_despesas(evento_id):
    caso = obter_caso(ListarDespesasService)
    return responder(caso.executar(evento_id))


@financeiro_controller.post("/eventos/<int:evento_id>/despesas")
@login_required
def adicionar_despesa(evento_id):
    caso = obter_caso(AdicionarDespesaService)
    return responder(
        caso.executar(evento_id, dados=request.get_json(silent=True) or {})
    )


@financeiro_controller.delete("/eventos/<int:evento_id>/despesas/<int:despesa_id>")
@login_required
def remover_despesa(evento_id, despesa_id):
    caso = obter_caso(RemoverDespesaService)
    return responder(caso.executar(evento_id, despesa_id))


@financeiro_controller.get("/eventos/<int:evento_id>/resumo")
@login_required
def resumo_evento(evento_id):
    caso = obter_caso(ResumoEventoService)
    return responder(caso.executar(evento_id))


@financeiro_controller.put("/eventos/<int:evento_id>/rateio")
@login_required
def definir_rateio(evento_id):
    caso = obter_caso(DefinirRateioService)
    return responder(
        caso.executar(evento_id, dados=request.get_json(silent=True) or {})
    )


@financeiro_controller.post(
    "/eventos/<int:evento_id>/despesas/<int:despesa_id>/comprovante"
)
@login_required
def enviar_comprovante(evento_id, despesa_id):
    caso = obter_caso(EnviarComprovanteService)
    return responder(
        caso.executar(evento_id, despesa_id, request.files.get("comprovante"))
    )
