from application.erros import NaoEncontrado
from models import PropostaFornecedor

from services.caso_uso import CasoUso


class RemoverPropostaService(CasoUso):
    def executar(self, evento_id, proposta_id):
        self.exigir_acesso_evento(evento_id, exigir_edicao=True)
        proposta = PropostaFornecedor.buscar_um(id=proposta_id, evento_id=evento_id)
        if not proposta:
            raise NaoEncontrado("Proposta não encontrada.")
        self.log(evento_id, "proposta_removida", proposta.fornecedor)
        proposta.deletar(confirmar=False)
        self.transacao.confirmar()
