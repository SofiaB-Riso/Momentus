from repositories.notificacao_repository import NotificacaoRepository

from services.caso_uso import CasoUso
from services.lembretes_service import GerarLembretesService


class ListarNotificacoesService(CasoUso):
    def executar(self):
        usuario = self.usuario_atual()
        GerarLembretesService().executar(usuario.id, transacao=self.transacao)
        itens = NotificacaoRepository.listar(usuario.id)
        return [n.to_dict() for n in itens]
