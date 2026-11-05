from application.erros import NaoEncontrado
from models import Convidado

from services.caso_uso import CasoUso
from services.convidados.dados_rsvp_service import MontarDadosRsvpService
from services.lembretes_service import GerarLembretesService


class VerRsvpService(CasoUso):
    def executar(self, token):
        convidado = Convidado.buscar_um(token_rsvp=token)
        if not convidado:
            raise NaoEncontrado("Convite inválido ou expirado.")
        GerarLembretesService().executar(
            evento_id=convidado.evento_id, transacao=self.transacao
        )
        return MontarDadosRsvpService().executar(convidado)
