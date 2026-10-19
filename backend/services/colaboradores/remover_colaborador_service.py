from application.erros import NaoEncontrado, Proibido
from models import ColaboradorEvento
from repositories.consulta_evento_repository import ConsultaEventoRepository

from services.caso_uso import CasoUso
from services.itens.liberacao_service import liberar_itens_colaborador


class RemoverColaboradorService(CasoUso):
    def executar(self, evento_id, colaborador_id):
        usuario, evento = self.exigir_acesso_evento(evento_id)
        if evento.owner_id != usuario.id:
            raise Proibido(
                "Somente a pessoa dona do evento pode remover colaboradores."
            )
        ConsultaEventoRepository.bloquear(evento.id)
        colab = ColaboradorEvento.buscar_um(id=colaborador_id, evento_id=evento.id)
        if not colab:
            raise NaoEncontrado("Colaborador não encontrado.")
        liberar_itens_colaborador(colab)
        colab.deletar(confirmar=False)
        self.log(evento.id, "colaborador_removido", colab.email)
        self.transacao.confirmar()
        return None
