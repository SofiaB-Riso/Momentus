from repositories.consulta_evento_repository import ConsultaEventoRepository
from services.caso_uso import CasoUso
from services.serializacao_evento import aplicar_permissoes, serializar_evento


class ListarEventosService(CasoUso):
    def executar(self):
        return self._preparar(self.usuario_atual().id)

    def _preparar(self, usuario_id):
        return [
            aplicar_permissoes(serializar_evento(e), e, usuario_id)
            for e in ConsultaEventoRepository.acessiveis(usuario_id)
        ]
