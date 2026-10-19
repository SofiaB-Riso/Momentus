from application.erros import NaoEncontrado, Proibido
from models import FotoEvento

from services.caso_uso import CasoUso


class RemoverFotoService(CasoUso):
    def __init__(self, transacao, usuario_id, armazenamento):
        super().__init__(transacao, usuario_id)
        self.armazenamento = armazenamento

    def executar(self, evento_id, foto_id):
        usuario, evento = self.exigir_acesso_evento(evento_id, exigir_edicao=True)
        foto = FotoEvento.buscar_um(id=foto_id, evento_id=evento.id)
        if not foto:
            raise NaoEncontrado("Foto não encontrada.")
        if evento.owner_id != usuario.id and foto.usuario_id != usuario.id:
            raise Proibido("Você não pode remover esta foto.")
        self.log(evento.id, "foto_removida", foto.legenda or "Foto do evento")
        nome = foto.arquivo
        foto.deletar(confirmar=False)
        self.transacao.confirmar()
        self.armazenamento.remover(nome)
        return None
