from application.erros import NaoEncontrado
from models import Convidado
from repositories.consulta_evento_repository import ConsultaEventoRepository

from services.caso_uso import CasoUso
from services.itens.liberacao_service import liberar_itens_convidado


class RemoverConvidadoService(CasoUso):
    def executar(self, evento_id, convidado_id):
        _, evento = self.exigir_acesso_evento(evento_id, exigir_edicao=True)
        ConsultaEventoRepository.bloquear(evento.id)
        convidado = Convidado.buscar_um(id=convidado_id, evento_id=evento.id)
        if not convidado:
            raise NaoEncontrado("Convidado não encontrado.")
        nome = convidado.nome
        liberar_itens_convidado(convidado)
        convidado.deletar(confirmar=False)
        self.log(evento.id, "convidado_removido", nome)
        self.transacao.confirmar()
        return None
