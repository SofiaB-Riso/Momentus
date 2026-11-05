from application.erros import NaoEncontrado
from models import Convidado

from services.caso_uso import CasoUso
from services.convidados.dados_rsvp_service import MontarDadosRsvpService


class ConsultarAtualizacaoRsvpService(CasoUso):
    def validar(self, token):
        if not Convidado.buscar_um(token_rsvp=token):
            raise NaoEncontrado("Convite inválido ou expirado.")

    def executar(self, token):
        convidado = Convidado.buscar_um(token_rsvp=token)
        return MontarDadosRsvpService().executar(convidado) if convidado else None
