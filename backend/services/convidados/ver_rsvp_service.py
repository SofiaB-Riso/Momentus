from application.erros import NaoEncontrado
from models import Convidado

from services.caso_uso import CasoUso
from services.convidados.dados_rsvp_service import dados_rsvp
from services.lembretes_service import gerar_lembretes


class VerRsvpService(CasoUso):
    def executar(self, token):
        convidado = Convidado.buscar_um(token_rsvp=token)
        if not convidado:
            raise NaoEncontrado("Convite inválido ou expirado.")
        gerar_lembretes(evento_id=convidado.evento_id, transacao=self.transacao)
        return dados_rsvp(convidado)
