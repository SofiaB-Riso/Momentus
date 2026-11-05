from application.erros import Proibido
from repositories.consulta_evento_repository import ConsultaEventoRepository
from services.caso_uso import CasoUso


class ListarLogsService(CasoUso):
    def executar(self, evento_id):
        usuario, evento = self.exigir_acesso_evento(evento_id)
        if evento.owner_id != usuario.id:
            raise Proibido("Histórico disponível apenas para a pessoa dona do evento.")
        logs = ConsultaEventoRepository.historico(evento.id)
        return [registro.to_dict() for registro in logs]
