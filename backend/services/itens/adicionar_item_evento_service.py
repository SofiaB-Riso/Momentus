from application.contratos import Criado
from application.erros import DadosInvalidos
from models import ItemEvento, Notificacao, ProdutoFornecedor
from utils.validacao import dinheiro, inteiro_positivo, validar_entrada

from services.caso_uso import CasoUso


class AdicionarItemEventoService(CasoUso):
    def executar(self, evento_id, dados=None):
        dados = validar_entrada(dados)
        _, evento = self.exigir_acesso_evento(evento_id, exigir_edicao=True)
        chave = str(
            dados.get("produtoId") or dados.get("produto_id") or dados.get("nome") or ""
        ).strip()
        try:
            quantidade = inteiro_positivo(dados.get("qtd", 1))
            if "preco" in dados:
                dinheiro(dados["preco"])
        except ValueError as erro:
            raise DadosInvalidos(str(erro))
        existente = (
            ItemEvento.buscar_um(evento_id=evento.id, chave_externa=chave)
            if chave
            else None
        )
        if existente:
            existente.quantidade += quantidade
            self.log(evento.id, "item_catalogo_atualizado", existente.nome)
            self.transacao.confirmar()
            return existente.to_dict()
        produto_id = (
            int(dados["produto_id"])
            if str(dados.get("produto_id") or "").isdigit()
            else None
        )
        produto = ProdutoFornecedor.buscar_por_id(produto_id) if produto_id else None
        item = ItemEvento(
            evento_id=evento.id,
            produto_id=produto.id if produto else None,
            chave_externa=chave or None,
            nome=(dados.get("nome") or (produto.nome if produto else "Item")).strip(),
            categoria=(
                dados.get("categoria") or (produto.categoria if produto else "outros")
            ).strip(),
            preco=dinheiro(
                dados.get("preco")
                if dados.get("preco") is not None
                else produto.preco
                if produto
                else 0
            ),
            quantidade=quantidade,
        )
        item.salvar(confirmar=False)
        self.transacao.sincronizar()
        self.log(evento.id, "item_catalogo_adicionado", item.nome)
        if float(evento.orcamento_evento or 0) > 0 and evento.total_despesas > float(
            evento.orcamento_evento or 0
        ):
            Notificacao(
                usuario_id=evento.owner_id,
                tipo="orcamento-ultrapassado",
                titulo="Teto de gastos ultrapassado",
                mensagem=f"{evento.nome_evento} ultrapassou o orçamento após adicionar {item.nome}.",
                evento_id=evento.id,
                referencia_id=item.id,
            ).salvar(confirmar=False)
        self.transacao.confirmar()
        return Criado(item.to_dict())
