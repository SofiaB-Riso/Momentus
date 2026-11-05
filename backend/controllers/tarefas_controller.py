from flask import Blueprint
from services.tarefas.adicionar_tarefa_service import AdicionarTarefaService
from services.tarefas.atualizar_tarefa_service import AtualizarTarefaService
from services.tarefas.remover_tarefa_service import RemoverTarefaService
from utils.auth import login_required

from controllers.contexto import obter_caso
from controllers.registro import registrar_controller
from controllers.respostas import ler_json, responder

tarefas_controller = Blueprint("tarefas_controller", __name__)


class TarefasController:
    """Adaptador HTTP do recurso; regras de negócio ficam nos Services."""

    @login_required
    def adicionar_tarefa(self, evento_id):
        caso = obter_caso(AdicionarTarefaService)
        return responder(caso.executar(evento_id, dados=ler_json()))

    @login_required
    def atualizar_tarefa(self, evento_id, tarefa_id):
        caso = obter_caso(AtualizarTarefaService)
        return responder(caso.executar(evento_id, tarefa_id, dados=ler_json()))

    @login_required
    def remover_tarefa(self, evento_id, tarefa_id):
        caso = obter_caso(RemoverTarefaService)
        return responder(caso.executar(evento_id, tarefa_id))


registrar_controller(
    tarefas_controller,
    TarefasController,
    [
        ("POST", "/eventos/<int:evento_id>/tarefas", "adicionar_tarefa"),
        ("PUT", "/eventos/<int:evento_id>/tarefas/<int:tarefa_id>", "atualizar_tarefa"),
        (
            "DELETE",
            "/eventos/<int:evento_id>/tarefas/<int:tarefa_id>",
            "remover_tarefa",
        ),
    ],
)
