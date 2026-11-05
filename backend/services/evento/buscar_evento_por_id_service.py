from services.caso_uso import CasoUso
from services.serializacao_evento import aplicar_permissoes, serializar_evento
from utils.validacao import validar_entrada


class BuscarEventoPorIdService(CasoUso):
    def executar(self, evento_id, dados=None):
        validar_entrada(dados)
        usuario, evento = self.exigir_acesso_evento(evento_id)
        return aplicar_permissoes(serializar_evento(evento), evento, usuario.id)
