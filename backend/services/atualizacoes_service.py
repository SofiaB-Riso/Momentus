from application.erros import NaoEncontrado
from models import Convidado
from repositories.consulta_evento_repository import ConsultaEventoRepository

from services.caso_uso import CasoUso
from services.convidados.dados_rsvp_service import dados_rsvp
from services.serializacao_evento import aplicar_permissoes, serializar_evento


class AtualizacoesService(CasoUso):
    def validar_evento(self, evento_id):
        self.exigir_acesso_evento(evento_id)

    def validar_rsvp(self, token):
        if not Convidado.buscar_um(token_rsvp=token):
            raise NaoEncontrado("Convite inválido ou expirado.")

    def evento(self, evento_id):
        usuario, evento = self.acesso_evento(evento_id)
        if evento is None or evento is False:
            return None
        return {
            "evento": aplicar_permissoes(serializar_evento(evento), evento, usuario.id),
            "log": ConsultaEventoRepository.revisao(evento.id),
        }

    def rsvp(self, token):
        convidado = Convidado.buscar_um(token_rsvp=token)
        return dados_rsvp(convidado) if convidado else None
