from flask import Blueprint, request
from services.tarefas.adicionar_tarefa_service import AdicionarTarefaService
from services.tarefas.atualizar_tarefa_service import AtualizarTarefaService
from services.tarefas.remover_tarefa_service import RemoverTarefaService
from utils.auth import login_required

from controllers.contexto import obter_caso
from controllers.respostas import responder

tarefas_controller = Blueprint("tarefas_controller", __name__)


@tarefas_controller.post("/eventos/<int:evento_id>/tarefas")
@login_required
def adicionar_tarefa(evento_id):
    caso = obter_caso(AdicionarTarefaService)
    return responder(
        caso.executar(evento_id, dados=request.get_json(silent=True) or {})
    )


@tarefas_controller.put("/eventos/<int:evento_id>/tarefas/<int:tarefa_id>")
@login_required
def atualizar_tarefa(evento_id, tarefa_id):
    caso = obter_caso(AtualizarTarefaService)
    return responder(
        caso.executar(evento_id, tarefa_id, dados=request.get_json(silent=True) or {})
    )


@tarefas_controller.delete("/eventos/<int:evento_id>/tarefas/<int:tarefa_id>")
@login_required
def remover_tarefa(evento_id, tarefa_id):
    caso = obter_caso(RemoverTarefaService)
    return responder(caso.executar(evento_id, tarefa_id))
