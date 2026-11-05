from datetime import datetime

from application.erros import NaoEncontrado
from models import TarefaEvento
from utils.validacao import validar_entrada

from services.caso_uso import CasoUso
from services.evento_comum import _recalcular_progresso


class AtualizarTarefaService(CasoUso):
    def executar(self, evento_id, tarefa_id, dados=None):
        dados = validar_entrada(dados)
        _, evento = self.exigir_acesso_evento(evento_id, exigir_edicao=True)
        tarefa = TarefaEvento.buscar_um(id=tarefa_id, evento_id=evento.id)
        if not tarefa:
            raise NaoEncontrado("Tarefa não encontrada.")
        if "feita" in dados:
            tarefa.feita = bool(dados["feita"])
        if "titulo" in dados:
            tarefa.titulo = (dados.get("titulo") or tarefa.titulo).strip()
        if "prazo" in dados:
            tarefa.prazo = (
                datetime.fromisoformat(dados["prazo"]) if dados.get("prazo") else None
            )
        self.log(
            evento.id,
            "tarefa_atualizada",
            f"{tarefa.titulo}: {('concluída' if tarefa.feita else 'pendente')}",
        )
        _recalcular_progresso(evento)
        self.transacao.confirmar()
        return {"tarefa": tarefa.to_dict(), "progresso": evento.progresso}
