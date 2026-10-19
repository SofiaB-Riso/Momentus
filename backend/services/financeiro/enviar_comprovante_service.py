from application.contratos import ArmazenamentoArquivos
from application.erros import NaoEncontrado
from models import DespesaEvento

from services.caso_uso import CasoUso


class EnviarComprovanteService(CasoUso):
    def __init__(self, transacao, usuario_id, armazenamento: ArmazenamentoArquivos):
        super().__init__(transacao, usuario_id)
        self.armazenamento = armazenamento

    def executar(self, evento_id, despesa_id, arquivo):
        _, evento = self.exigir_acesso_evento(evento_id, exigir_edicao=True)
        despesa = DespesaEvento.buscar_um(id=despesa_id, evento_id=evento.id)
        if not despesa:
            raise NaoEncontrado("Despesa não encontrada.")
        nome = self.armazenamento.salvar(
            arquivo,
            f"comprovante_evento{evento.id}_{despesa.id}",
            {"png", "jpg", "jpeg", "webp", "gif", "pdf"},
        )
        anterior = despesa.comprovante
        try:
            despesa.atualizar(confirmar=False, comprovante=nome)
            self.log(evento.id, "comprovante_enviado", despesa.descricao)
            self.transacao.confirmar()
        except Exception:
            self.transacao.reverter()
            self.armazenamento.remover(nome)
            raise
        self.armazenamento.remover(anterior)
        return despesa.to_dict()
