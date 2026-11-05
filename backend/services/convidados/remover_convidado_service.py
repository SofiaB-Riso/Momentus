from application.erros import NaoEncontrado
from models import Convidado
from repositories.consulta_evento_repository import ConsultaEventoRepository

from services.caso_uso import CasoUso
from services.itens.liberacao_service import LiberarItensConvidadoService
from services.lista_espera.organizar_fila_service import OrganizarFilaService


class RemoverConvidadoService(CasoUso):
    def executar(self, evento_id, convidado_id):
        _, evento = self.exigir_acesso_evento(evento_id, exigir_edicao=True)
        ConsultaEventoRepository.bloquear(evento.id)
        convidado = Convidado.buscar_um(id=convidado_id, evento_id=evento.id)
        if not convidado:
            raise NaoEncontrado("Convidado não encontrado.")
        nome = convidado.nome
        LiberarItensConvidadoService().executar(convidado)
        convidado.deletar(confirmar=False)
        self.transacao.sincronizar()
        OrganizarFilaService().promover(evento)
        self.log(evento.id, "convidado_removido", nome)
        self.transacao.confirmar()
        return None
