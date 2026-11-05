from models import PlanejamentoEvento
from models.tempo import utcnow
from repositories.consulta_evento_repository import ConsultaEventoRepository

from services.caso_uso import CasoUso
from services.cronograma.sincronizar_cronograma_service import (
    SincronizarCronogramaService,
)


class GerarCronogramaService(CasoUso):
    def executar(self, evento_id):
        _, evento = self.exigir_acesso_evento(evento_id, exigir_edicao=True)
        ConsultaEventoRepository.bloquear(evento.id)
        if not evento.planejamento:
            evento.planejamento = PlanejamentoEvento(evento_id=evento.id).salvar(
                confirmar=False
            )
        evento.planejamento.cronograma_ativo = True
        evento.planejamento.cronograma_gerado_em = utcnow()
        alteradas = SincronizarCronogramaService().executar(evento, adicionar=True)
        self.log(
            evento.id,
            "cronograma_gerado",
            f"{len(alteradas)} tarefa(s) pendente(s) com prazos sugeridos.",
        )
        self.transacao.confirmar()
        return {
            "alteradas": len(alteradas),
            "tarefas": [t.to_dict() for t in alteradas],
            "mensagem": "Cronograma distribuído entre agora e o evento. Prazos automáticos pendentes acompanham mudanças da data ou do tipo. Tarefas concluídas e manuais são preservadas.",
        }
