from application.contratos import Criado
from application.erros import DadosInvalidos
from models import DespesaEvento, Notificacao
from utils.validacao import dinheiro, validar_entrada

from services.caso_uso import CasoUso
from services.financeiro.resumo_financeiro_service import resumo_financeiro


class AdicionarDespesaService(CasoUso):
    def executar(self, evento_id, dados=None):
        dados = validar_entrada(dados)
        usuario, evento = self.exigir_acesso_evento(evento_id, exigir_edicao=True)
        descricao = (dados.get("descricao") or "").strip()
        try:
            valor = dinheiro(dados.get("valor") or 0)
        except ValueError as erro:
            raise DadosInvalidos(str(erro))
        if not descricao or valor <= 0:
            raise DadosInvalidos("Informe descrição e valor maior que zero.")
        despesa = DespesaEvento(
            evento_id=evento.id,
            descricao=descricao,
            categoria=(dados.get("categoria") or "geral").strip(),
            valor=valor,
            comprovante=(dados.get("comprovante") or "").strip(),
            pago_por=(dados.get("pago_por") or usuario.nome).strip(),
        )
        despesa.salvar(confirmar=False)
        self.transacao.sincronizar()
        self.log(evento.id, "despesa_adicionada", f"{descricao}: {valor:.2f}")
        if float(evento.orcamento_evento or 0) > 0 and evento.total_despesas > float(
            evento.orcamento_evento or 0
        ):
            Notificacao(
                usuario_id=evento.owner_id,
                tipo="orcamento-ultrapassado",
                titulo="Teto de gastos ultrapassado",
                mensagem=f"{evento.nome_evento} ultrapassou o orçamento definido.",
                evento_id=evento.id,
                referencia_id=despesa.id,
            ).salvar(confirmar=False)
        self.transacao.confirmar()
        return Criado(
            {"despesa": despesa.to_dict(), "resumo": resumo_financeiro(evento)}
        )
