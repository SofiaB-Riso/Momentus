from application.erros import NaoEncontrado
from repositories.arquivo_repository import ArquivoRepository

from services.caso_uso import CasoUso


class AcessarArquivoService(CasoUso):
    def executar(self, nome):
        avatar, registro = ArquivoRepository.referencias(nome)
        if avatar and avatar.usuario_id == self.usuario_id:
            return nome
        if registro:
            _, evento = self.acesso_evento(registro.evento_id)
            if evento:
                return nome
        raise NaoEncontrado("Arquivo não encontrado.")
