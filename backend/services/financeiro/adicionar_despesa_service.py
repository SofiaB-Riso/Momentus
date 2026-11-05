import json
from hashlib import sha256
from uuid import UUID

from application.contratos import Criado
from application.erros import Conflito, DadosInvalidos
from models import DespesaEvento, Notificacao, RequisicaoDespesa
from repositories.consulta_evento_repository import ConsultaEventoRepository
from repositories.requisicao_despesa_repository import RequisicaoDespesaRepository
from utils.validacao import dinheiro, validar_entrada

from services.caso_uso import CasoUso
from services.financeiro.resumo_financeiro_service import (
    CalcularResumoFinanceiroService,
)


class AdicionarDespesaService(CasoUso):
    def executar(self, evento_id, dados=None, chave_requisicao=None):
        dados = validar_entrada(dados)
        usuario, evento = self.exigir_acesso_evento(evento_id, exigir_edicao=True)
        descricao = (dados.get("descricao") or "").strip()
        if dados.get("comprovante"):
            raise DadosInvalidos(
                "Anexe o comprovante pelo envio de arquivo da despesa."
            )
        try:
            valor = dinheiro(dados.get("valor") or 0)
        except ValueError as erro:
            raise DadosInvalidos(str(erro))
        if not descricao or valor <= 0:
            raise DadosInvalidos("Informe descrição e valor maior que zero.")
        categoria = (dados.get("categoria") or "geral").strip()
        pago_por = (dados.get("pago_por") or usuario.nome).strip()
        assinatura = sha256(
            json.dumps(
                [evento.id, descricao, str(valor), categoria, pago_por],
                ensure_ascii=False,
            ).encode()
        ).hexdigest()
        if chave_requisicao:
            try:
                if not isinstance(chave_requisicao, str) or len(chave_requisicao) > 36:
                    raise ValueError()
                chave_requisicao = str(UUID(chave_requisicao))
            except (ValueError, TypeError, AttributeError):
                raise DadosInvalidos("Chave de envio inválida.") from None
            RequisicaoDespesaRepository.bloquear_usuario(usuario.id)
            ConsultaEventoRepository.bloquear(evento.id)
            anterior = RequisicaoDespesaRepository.por_chave(
                usuario.id, chave_requisicao
            )
            if anterior:
                if anterior.assinatura != assinatura or anterior.despesa_id is None:
                    raise Conflito(
                        "Este envio já foi usado. Atualize a tela antes de registrar outra despesa."
                    )
                despesa = DespesaEvento.buscar_por_id(anterior.despesa_id)
                return Criado(
                    {
                        "despesa": despesa.to_dict(),
                        "resumo": CalcularResumoFinanceiroService().executar(evento),
                    }
                )
        despesa = DespesaEvento(
            evento_id=evento.id,
            descricao=descricao,
            categoria=categoria,
            valor=valor,
            comprovante="",
            pago_por=pago_por,
        )
        despesa.salvar(confirmar=False)
        self.transacao.sincronizar()
        if chave_requisicao:
            RequisicaoDespesa(
                usuario_id=usuario.id,
                evento_id=evento.id,
                despesa_id=despesa.id,
                chave=chave_requisicao,
                assinatura=assinatura,
            ).salvar(confirmar=False)
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
            {
                "despesa": despesa.to_dict(),
                "resumo": CalcularResumoFinanceiroService().executar(evento),
            }
        )
