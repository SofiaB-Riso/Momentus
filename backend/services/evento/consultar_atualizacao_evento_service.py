from application.erros import Proibido
from repositories.consulta_evento_repository import ConsultaEventoRepository
from services.caso_uso import CasoUso
from services.serializacao_evento import aplicar_permissoes, serializar_evento


class ConsultarAtualizacaoEventoService(CasoUso):
    def validar(self, evento_id):
        self.exigir_acesso_evento(evento_id)

    def executar(self, evento_id):
        try:
            usuario, evento = self.acesso_evento(evento_id)
        except Proibido:
            return None
        if evento is None or evento is False:
            return None
        return {
            "evento": aplicar_permissoes(serializar_evento(evento), evento, usuario.id),
            "log": ConsultaEventoRepository.revisao(evento.id),
        }
