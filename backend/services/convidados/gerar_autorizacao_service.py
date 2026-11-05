from datetime import timedelta
from hashlib import sha256
from secrets import token_urlsafe

from application.erros import DadosInvalidos, NaoEncontrado
from models import Convidado
from models.tempo import utcnow
from repositories.consulta_evento_repository import ConsultaEventoRepository

from services.caso_uso import CasoUso
from services.convidados.informacoes_alimentares_service import (
    RegistrarInformacoesAlimentaresService,
)
from services.lista_espera.organizar_fila_service import OrganizarFilaService


class GerarLinkResponsavelConvidadoService(CasoUso):
    def executar(self, token):
        convidado = Convidado.buscar_um(token_rsvp=token)
        if not convidado:
            raise NaoEncontrado("Convite não encontrado.")
        ConsultaEventoRepository.bloquear(convidado.evento_id)
        RegistrarInformacoesAlimentaresService().executar(
            convidado, {"faixa_etaria": "menor"}, "rsvp"
        )
        registro = convidado.consentimento
        if registro.vigente:
            raise DadosInvalidos(
                "Revogue a autorização atual antes de solicitar outra."
            )
        convidado.status = "pendente"
        OrganizarFilaService().cancelar(convidado)
        OrganizarFilaService().promover(convidado.evento)
        from services.itens.liberacao_service import LiberarItensConvidadoService

        LiberarItensConvidadoService().executar(convidado)
        registro.saude = ""
        registro.revogado_em = utcnow()
        segredo = token_urlsafe(32)
        registro.token_hash = sha256(segredo.encode()).hexdigest()
        registro.expira_em = utcnow() + timedelta(days=7)
        self.transacao.confirmar()
        return {
            "link": "/autorizacao.html#tipo=convidado&token=" + segredo,
            "validade_dias": 7,
        }
