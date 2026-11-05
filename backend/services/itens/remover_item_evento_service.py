from application.erros import NaoEncontrado
from models import ItemEvento

from services.caso_uso import CasoUso


class RemoverItemEventoService(CasoUso):
    def executar(self, evento_id, item_id):
        _, evento = self.exigir_acesso_evento(evento_id, exigir_edicao=True)
        item = ItemEvento.buscar_um(id=item_id, evento_id=evento.id)
        if not item:
            raise NaoEncontrado("Item não encontrado.")
        self.log(evento.id, "item_catalogo_removido", item.nome)
        item.deletar(confirmar=False)
        self.transacao.confirmar()
        return None
