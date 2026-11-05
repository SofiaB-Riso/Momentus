from application.contratos import Transacao
from application.erros import NaoEncontrado, Proibido
from models import Usuario

from services.acesso_service import VerificarAcessoEventoService
from services.conta.verificar_autorizacao_service import (
    VerificarAutorizacaoContaService,
)


class CasoUso:
    """Contexto explícito: serviços não leem request, sessão ou current_app."""

    def __init__(self, transacao: Transacao, usuario_id=None):
        self.transacao = transacao
        self.usuario_id = usuario_id

    def usuario_atual(self, exigir_autorizacao=True):
        usuario = (
            Usuario.buscar_um(id=self.usuario_id, ativo=True)
            if self.usuario_id
            else None
        )
        if usuario and exigir_autorizacao:
            VerificarAutorizacaoContaService().executar(usuario)
        return usuario

    def acesso_evento(self, evento_id, exigir_edicao=False):
        return VerificarAcessoEventoService().executar(
            self.usuario_id, evento_id, exigir_edicao
        )

    def exigir_acesso_evento(self, evento_id, exigir_edicao=False):
        usuario, evento = self.acesso_evento(evento_id, exigir_edicao)
        if evento is None:
            raise NaoEncontrado("Evento não encontrado.")
        if evento is False:
            raise Proibido("Você não tem acesso a este evento.")
        return usuario, evento

    def log(self, evento_id, acao, detalhe=""):
        from models import LogEvento

        LogEvento(
            evento_id=evento_id, usuario_id=self.usuario_id, acao=acao, detalhe=detalhe
        ).salvar(confirmar=False)
