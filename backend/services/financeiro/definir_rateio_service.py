from application.erros import DadosInvalidos
from utils.validacao import dinheiro, validar_entrada

from services.caso_uso import CasoUso
from services.financeiro.resumo_financeiro_service import resumo_financeiro


class DefinirRateioService(CasoUso):
    def executar(self, evento_id, dados=None):
        dados = validar_entrada(dados)
        _, evento = self.exigir_acesso_evento(evento_id, exigir_edicao=True)
        if "modo" in dados and dados["modo"] not in {"auto", "fixo"}:
            raise DadosInvalidos("Escolha rateio automático ou fixo.")
        try:
            valor = dinheiro(dados.get("valorFixo", evento.rateio_valor_fixo or 0))
        except ValueError as erro:
            raise DadosInvalidos(str(erro))
        if "ativo" in dados:
            if not isinstance(dados["ativo"], bool):
                raise DadosInvalidos("Ativo deve ser verdadeiro ou falso.")
            evento.rateio_ativo = dados["ativo"]
        evento.rateio_modo = dados.get("modo", evento.rateio_modo)
        evento.rateio_valor_fixo = valor
        self.log(
            evento.id,
            "rateio_atualizado",
            f"{('Ativado' if evento.rateio_ativo else 'Desativado')}; {('automático' if evento.rateio_modo == 'auto' else 'fixo')}; valor fixo: R$ {valor:.2f}",
        )
        self.transacao.confirmar()
        return resumo_financeiro(evento)["rateio"]
