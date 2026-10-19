from application.contratos import ArmazenamentoArquivos
from application.erros import Proibido
from models import Evento
from services.caso_uso import CasoUso
from services.galeria.arquivos_evento_service import arquivos_do_evento
from sqlalchemy.exc import SQLAlchemyError


class DeletarEventoService(CasoUso):
    def __init__(self, transacao, usuario_id, armazenamento: ArmazenamentoArquivos):
        super().__init__(transacao, usuario_id)
        self.armazenamento = armazenamento

    def executar(self, evento_id):
        usuario, evento = self.exigir_acesso_evento(evento_id)
        if evento.owner_id != usuario.id:
            raise Proibido("Somente a pessoa dona do evento pode excluí-lo.")
        try:
            arquivos = arquivos_do_evento(evento_id)
            self._preparar(evento_id)
            self.transacao.confirmar()
            for arquivo in arquivos:
                self.armazenamento.remover(arquivo)
            return None
        except SQLAlchemyError:
            self.transacao.reverter()
            raise

    def _preparar(self, evento_id):
        evento = Evento.buscar_por_id(evento_id)
        if evento is None:
            return False
        evento.deletar(confirmar=False)
        self.transacao.sincronizar()
        return True
