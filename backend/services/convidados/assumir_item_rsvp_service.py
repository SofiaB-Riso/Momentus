from application.erros import Conflito, DadosInvalidos, NaoEncontrado
from models import Convidado, ItemCompartilhado, LogEvento
from repositories.consulta_evento_repository import ConsultaEventoRepository
from repositories.item_repository import ItemRepository

from services.caso_uso import CasoUso
from services.notificacoes_service import notificar_organizacao


class AssumirItemRsvpService(CasoUso):
    def executar(self, token, item_id):
        convidado = Convidado.buscar_um(token_rsvp=token)
        if not convidado:
            raise NaoEncontrado("Convite inválido ou expirado.")
        ConsultaEventoRepository.bloquear(convidado.evento_id)
        item = ItemCompartilhado.buscar_um(id=item_id, evento_id=convidado.evento_id)
        if not item:
            raise NaoEncontrado("Item não encontrado.")
        if convidado.status == "recusado":
            raise DadosInvalidos("Atualize sua presença antes de assumir um item.")
        if item.responsavel_tipo == "convidado" and item.responsavel_id == convidado.id:
            return item.to_dict()
        alterados = ItemRepository.reservar_convidado(
            item.id, convidado.evento_id, convidado
        )
        if not alterados:
            self.transacao.reverter()
            raise Conflito(
                "Este item já foi reservado por outra pessoa. Atualize a lista."
            )
        notificar_organizacao(
            convidado.evento,
            "item-assumido",
            "Item da lista assumido",
            f"{convidado.nome} ficou responsável por {item.nome}.",
            item.id,
        )
        LogEvento(
            evento_id=convidado.evento_id,
            acao="item_assumido",
            detalhe=f"{convidado.nome}: {item.nome}",
        ).salvar(confirmar=False)
        self.transacao.confirmar()
        return item.to_dict()
