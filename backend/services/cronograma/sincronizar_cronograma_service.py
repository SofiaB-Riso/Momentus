from datetime import datetime, time, timedelta

from application.erros import DadosInvalidos
from models import TarefaEvento
from utils.tempo_local import agora_local
from utils.validacao import normalizar

from services.cronograma.regras import PADRAO, PERFIS, REGRAS
from services.evento_comum import _recalcular_progresso


class SincronizarCronogramaService:
    def executar(self, evento, adicionar=False):
        config = evento.planejamento
        if not config or not config.cronograma_ativo:
            return []
        perfil = PERFIS.get(normalizar(evento.tipo_evento), PADRAO)
        agora = agora_local()
        fim = datetime.combine(
            evento.data_evento,
            time.fromisoformat(evento.hora_evento)
            if evento.hora_evento
            else time(23, 59, 59),
        )
        if fim <= agora:
            if adicionar:
                raise DadosInvalidos(
                    "O evento já começou ou passou. Escolha uma data e um horário futuros para gerar o cronograma."
                )
            # Uma data passada pode ser registrada no histórico sem criar novos prazos.
            return []
        dias = (evento.data_evento - agora.date()).days
        maior, menor = max(perfil), min(perfil)
        if dias < maior:
            # Comprime o perfil inteiro para distribuir as etapas no tempo disponível,
            # em vez de fixar todos os prazos atrasados na mesma data.
            antecedencias = [
                1 + round((dias - 1) * (valor - menor) / (maior - menor))
                if dias > 0
                else 0
                for valor in perfil
            ]
        else:
            antecedencias = perfil
        existentes = {
            t.chave: t for t in TarefaEvento.listar(evento_id=evento.id) if t.chave
        }
        alteradas = []
        for chave, titulo, indice in REGRAS:
            tarefa = existentes.get(chave)
            if not tarefa and adicionar:
                tarefa = TarefaEvento(
                    evento_id=evento.id, chave=chave, titulo=titulo
                ).salvar(confirmar=False)
            if tarefa and not tarefa.feita:
                sugerido = datetime.combine(evento.data_evento, time(9, 0)) - timedelta(
                    days=antecedencias[indice]
                )
                if dias == 0:
                    # Mesmo dia: usa o intervalo de horas restante até o início.
                    fracao = (maior - perfil[indice]) / (maior - menor)
                    sugerido = agora + (fim - agora) * fracao
                tarefa.prazo = min(fim, max(agora, sugerido))
                tarefa.ordem = 200 - perfil[indice]
                alteradas.append(tarefa)
        _recalcular_progresso(evento)
        return alteradas
