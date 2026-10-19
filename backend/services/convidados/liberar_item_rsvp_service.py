from application.erros import NaoEncontrado, Proibido
from models import Convidado, ItemCompartilhado, LogEvento
from repositories.consulta_evento_repository import ConsultaEventoRepository
from repositories.item_repository import ItemRepository

from services.caso_uso import CasoUso
from services.notificacoes_service import notificar_organizacao


class LiberarItemRsvpService(CasoUso):
    def executar(self, token, item_id):
        convidado = Convidado.buscar_um(token_rsvp=token)
        if not convidado:
            raise NaoEncontrado("Convite inválido ou expirado.")
        ConsultaEventoRepository.bloquear(convidado.evento_id)
        item = ItemCompartilhado.buscar_um(id=item_id, evento_id=convidado.evento_id)
        if not item:
            raise NaoEncontrado("Item não encontrado.")
        alterados = ItemRepository.liberar_convidado(item.id, convidado.id)
        if not alterados:
            self.transacao.reverter()
            raise Proibido("Você só pode liberar um item que assumiu.")
        notificar_organizacao(
            convidado.evento,
            "item-liberado",
            "Item disponível novamente",
            f"{convidado.nome} liberou {item.nome}.",
            item.id,
        )
        LogEvento(
            evento_id=convidado.evento_id,
            acao="item_liberado",
            detalhe=f"{convidado.nome}: {item.nome}",
        ).salvar(confirmar=False)
        self.transacao.confirmar()
        return item.to_dict()
