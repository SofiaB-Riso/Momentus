from repositories.notificacao_repository import NotificacaoRepository

from services.caso_uso import CasoUso


class MarcarNotificacoesLidasService(CasoUso):
    def executar(self):
        usuario = self.usuario_atual()
        NotificacaoRepository.marcar_lidas(usuario.id)
        self.transacao.confirmar()
        return None
