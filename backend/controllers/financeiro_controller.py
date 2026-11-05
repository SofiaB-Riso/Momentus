from flask import Blueprint, request
from services.financeiro.adicionar_despesa_service import AdicionarDespesaService
from services.financeiro.definir_rateio_service import DefinirRateioService
from services.financeiro.enviar_comprovante_service import EnviarComprovanteService
from services.financeiro.listar_despesas_service import ListarDespesasService
from services.financeiro.remover_despesa_service import RemoverDespesaService
from services.financeiro.resumo_evento_service import ResumoEventoService
from utils.auth import login_required

from controllers.contexto import obter_caso
from controllers.registro import registrar_controller
from controllers.respostas import ler_json, responder

financeiro_controller = Blueprint("financeiro_controller", __name__)


class FinanceiroController:
    """Adaptador HTTP do recurso; regras de negócio ficam nos Services."""

    @login_required
    def listar_despesas(self, evento_id):
        caso = obter_caso(ListarDespesasService)
        return responder(caso.executar(evento_id))

    @login_required
    def adicionar_despesa(self, evento_id):
        caso = obter_caso(AdicionarDespesaService)
        return responder(
            caso.executar(
                evento_id,
                dados=ler_json(),
                chave_requisicao=request.headers.get("Idempotency-Key"),
            )
        )

    @login_required
    def remover_despesa(self, evento_id, despesa_id):
        caso = obter_caso(RemoverDespesaService)
        return responder(caso.executar(evento_id, despesa_id))

    @login_required
    def resumo_evento(self, evento_id):
        caso = obter_caso(ResumoEventoService)
        return responder(caso.executar(evento_id))

    @login_required
    def definir_rateio(self, evento_id):
        caso = obter_caso(DefinirRateioService)
        return responder(caso.executar(evento_id, dados=ler_json()))

    @login_required
    def enviar_comprovante(self, evento_id, despesa_id):
        caso = obter_caso(EnviarComprovanteService)
        return responder(
            caso.executar(evento_id, despesa_id, request.files.get("comprovante"))
        )


registrar_controller(
    financeiro_controller,
    FinanceiroController,
    [
        ("GET", "/eventos/<int:evento_id>/despesas", "listar_despesas"),
        ("POST", "/eventos/<int:evento_id>/despesas", "adicionar_despesa"),
        (
            "DELETE",
            "/eventos/<int:evento_id>/despesas/<int:despesa_id>",
            "remover_despesa",
        ),
        ("GET", "/eventos/<int:evento_id>/resumo", "resumo_evento"),
        ("PUT", "/eventos/<int:evento_id>/rateio", "definir_rateio"),
        (
            "POST",
            "/eventos/<int:evento_id>/despesas/<int:despesa_id>/comprovante",
            "enviar_comprovante",
        ),
    ],
)
