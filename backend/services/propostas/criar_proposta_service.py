from application.contratos import Criado
from models import PropostaFornecedor

from services.caso_uso import CasoUso
from services.propostas.validacao import preparar


class CriarPropostaService(CasoUso):
    def executar(self, evento_id, dados):
        _, evento = self.exigir_acesso_evento(evento_id, exigir_edicao=True)
        proposta = PropostaFornecedor(evento_id=evento.id, **preparar(dados)).salvar(
            confirmar=False
        )
        self.transacao.sincronizar()
        self.log(evento.id, "proposta_criada", proposta.fornecedor)
        self.transacao.confirmar()
        return Criado(proposta.to_dict())
