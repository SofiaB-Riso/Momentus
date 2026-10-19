from application.erros import NaoEncontrado
from models import LocalEvento, LogEvento

from services.caso_uso import CasoUso


class RemoverLocalService(CasoUso):
    def executar(self, evento_id, local_id):
        usuario, evento = self.exigir_acesso_evento(evento_id, exigir_edicao=True)
        local = LocalEvento.buscar_um(evento_id=evento.id, id=local_id)
        if not local:
            raise NaoEncontrado("Espaço não encontrado.")
        LogEvento(
            evento_id=evento.id,
            usuario_id=usuario.id,
            acao="local_removido",
            detalhe=local.nome,
        ).salvar(confirmar=False)
        local.deletar(confirmar=False)
        self.transacao.confirmar()
        return None
