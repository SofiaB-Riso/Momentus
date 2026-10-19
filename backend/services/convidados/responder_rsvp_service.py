from application.erros import DadosInvalidos, NaoEncontrado
from models import Convidado, LogEvento
from repositories.consulta_evento_repository import ConsultaEventoRepository
from utils.validacao import validar_entrada

from services.caso_uso import CasoUso
from services.itens.liberacao_service import liberar_itens_convidado
from services.notificacoes_service import notificar_organizacao


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
        mudou = convidado.status != status or (
            "restricoes" in dados
            and convidado.restricoes_alimentares
            != str(dados.get("restricoes") or "").strip()
        )
        convidado.status = status
        if "restricoes" in dados:
            convidado.restricoes_alimentares = str(
                dados.get("restricoes") or ""
            ).strip()[:4000]
        if status == "recusado":
            liberar_itens_convidado(convidado)
        if mudou:
            notificar_organizacao(
                convidado.evento,
                "rsvp",
                "Resposta de convite",
                f"{convidado.nome} atualizou a presença para {status} e/ou as restrições alimentares.",
                convidado.id,
            )
            LogEvento(
                evento_id=convidado.evento_id,
                acao="rsvp_atualizado",
                detalhe=f"{convidado.nome}: presença {status}; informações alimentares atualizadas.",
            ).salvar(confirmar=False)
        self.transacao.confirmar()
        return {"convidado": convidado.to_dict(incluir_token=False)}
