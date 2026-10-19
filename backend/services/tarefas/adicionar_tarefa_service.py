from datetime import datetime

from application.contratos import Criado
from application.erros import DadosInvalidos
from models import TarefaEvento
from utils.validacao import validar_entrada

from services.caso_uso import CasoUso


class AdicionarTarefaService(CasoUso):
    def executar(self, evento_id, dados=None):
        dados = validar_entrada(dados)
        _, evento = self.exigir_acesso_evento(evento_id, exigir_edicao=True)
        titulo = (dados.get("titulo") or "").strip()
        if not titulo:
            raise DadosInvalidos("Título da tarefa é obrigatório.")
        prazo = None
        if dados.get("prazo"):
            prazo = datetime.fromisoformat(dados["prazo"])
        tarefa = TarefaEvento(
            evento_id=evento.id,
            titulo=titulo,
            prazo=prazo,
            ordem=len(evento.tarefas_rel),
        )
        tarefa.salvar(confirmar=False)
        self.log(evento.id, "tarefa_adicionada", titulo)
        self.transacao.confirmar()
        return Criado(tarefa.to_dict())
