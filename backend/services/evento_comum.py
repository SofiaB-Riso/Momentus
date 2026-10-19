def _recalcular_progresso(evento):
    from models import TarefaEvento

    tarefas = TarefaEvento.listar(evento_id=evento.id)
    evento.progresso = (
        round(100 * sum((t.feita for t in tarefas)) / len(tarefas)) if tarefas else 0
    )
