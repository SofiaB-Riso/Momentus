from application.erros import NaoEncontrado
from models import TarefaEvento

from services.caso_uso import CasoUso
from services.evento_comum import _recalcular_progresso


class RemoverTarefaService(CasoUso):
    def executar(self, evento_id, tarefa_id):
        _, evento = self.exigir_acesso_evento(evento_id, exigir_edicao=True)
        tarefa = TarefaEvento.buscar_um(id=tarefa_id, evento_id=evento.id)
        if not tarefa:
            raise NaoEncontrado("Tarefa não encontrada.")
        self.log(evento.id, "tarefa_removida", tarefa.titulo)
        tarefa.deletar(confirmar=False)
        self.transacao.sincronizar()
        _recalcular_progresso(evento)
        self.transacao.confirmar()
        return None
