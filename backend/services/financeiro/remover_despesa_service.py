from application.contratos import ArmazenamentoArquivos
from application.erros import NaoEncontrado
from models import DespesaEvento

from services.caso_uso import CasoUso


class RemoverDespesaService(CasoUso):
    def __init__(self, transacao, usuario_id, armazenamento: ArmazenamentoArquivos):
        super().__init__(transacao, usuario_id)
        self.armazenamento = armazenamento

    def executar(self, evento_id, despesa_id):
        _, evento = self.exigir_acesso_evento(evento_id, exigir_edicao=True)
        despesa = DespesaEvento.buscar_um(id=despesa_id, evento_id=evento.id)
        if not despesa:
            raise NaoEncontrado("Despesa não encontrada.")
        self.log(evento.id, "despesa_removida", despesa.descricao)
        comprovante = despesa.comprovante
        despesa.deletar(confirmar=False)
        self.transacao.confirmar()
        self.armazenamento.remover(comprovante)
        return None
