from application.erros import NaoEncontrado
from models import PropostaFornecedor

from services.caso_uso import CasoUso
from services.propostas.validacao import preparar


class AtualizarPropostaService(CasoUso):
    def executar(self, evento_id, proposta_id, dados):
        self.exigir_acesso_evento(evento_id, exigir_edicao=True)
        proposta = PropostaFornecedor.buscar_um(id=proposta_id, evento_id=evento_id)
        if not proposta:
            raise NaoEncontrado("Proposta não encontrada.")
        proposta.atualizar(confirmar=False, **preparar(dados))
        self.log(evento_id, "proposta_atualizada", proposta.fornecedor)
        self.transacao.confirmar()
        return proposta.to_dict()
