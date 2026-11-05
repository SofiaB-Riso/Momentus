from application.erros import DadosInvalidos, NaoEncontrado
from models import Convidado, LogEvento
from repositories.consulta_evento_repository import ConsultaEventoRepository
from utils.validacao import validar_entrada

from services.caso_uso import CasoUso
from services.convidados.informacoes_alimentares_service import (
    RegistrarInformacoesAlimentaresService,
)
from services.itens.liberacao_service import LiberarItensConvidadoService
from services.lista_espera.organizar_fila_service import OrganizarFilaService
from services.notificacoes_service import NotificarOrganizacaoService


class ResponderRsvpService(CasoUso):
    def executar(self, token, dados=None):
        dados = validar_entrada(dados)
        convidado = Convidado.buscar_um(token_rsvp=token)
        if not convidado:
            raise NaoEncontrado("Convite inválido ou expirado.")
        ConsultaEventoRepository.bloquear(convidado.evento_id)
        status = dados.get("status")
        if status not in {"confirmado", "recusado", "pendente"}:
            raise DadosInvalidos("Status de RSVP inválido.")
        mudou = (
            convidado.status != status
            or bool({"saude", "revogar_saude", "faixa_etaria"}.intersection(dados))
            or (
                "restricoes" in dados
                and convidado.restricoes_alimentares
                != str(dados.get("restricoes") or "").strip()
            )
        )
        RegistrarInformacoesAlimentaresService().executar(convidado, dados, "rsvp")
        if (
            convidado.consentimento
            and convidado.consentimento.faixa_etaria == "menor"
            and convidado.consentimento.responsavel_autorizou is not True
            and status != "recusado"
        ):
            raise DadosInvalidos(
                "Peça ao responsável legal para autorizar sua participação pelo link privado antes de enviar a resposta."
            )
        if status == "recusado":
            RegistrarInformacoesAlimentaresService().executar(
                convidado, {"revogar_saude": True}, "rsvp"
            )
            LiberarItensConvidadoService().executar(convidado)
        OrganizarFilaService().aplicar(convidado, status)
        if mudou:
            NotificarOrganizacaoService().executar(
                convidado.evento,
                "rsvp",
                "Resposta de convite",
                f"{convidado.nome} atualizou a presença para {convidado.status} e/ou as restrições alimentares.",
                convidado.id,
            )
            LogEvento(
                evento_id=convidado.evento_id,
                acao="rsvp_atualizado",
                detalhe=f"{convidado.nome}: presença {convidado.status}; informações alimentares atualizadas.",
            ).salvar(confirmar=False)
        self.transacao.confirmar()
        return {"convidado": convidado.to_dict(incluir_token=False)}
