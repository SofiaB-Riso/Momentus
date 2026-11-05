import json
from decimal import Decimal

from application.erros import DadosInvalidos
from utils.validacao import dinheiro, validar_entrada, validar_nome

CATEGORIAS = {"buffet", "decoracao", "musica", "doces", "bebidas", "espacos", "outros"}
SERVICOS = {"equipe", "montagem", "transporte", "limpeza", "materiais"}


def preparar(dados):
    dados = validar_entrada(dados)
    nome = validar_nome(dados.get("fornecedor"))
    categoria = dados.get("categoria")
    if not isinstance(categoria, str) or categoria not in CATEGORIAS:
        raise DadosInvalidos(
            "Selecione uma categoria válida para comparar propostas equivalentes."
        )
    valor, desconto, taxas = (
        dinheiro(dados.get(k, 0)) for k in ("valor", "desconto", "taxas")
    )
    if (
        valor <= 0
        or desconto > valor
        or valor - desconto + taxas > Decimal("99999999.99")
    ):
        raise DadosInvalidos("Confira o preço, o desconto e as taxas da proposta.")
    parcelas = dados.get("parcelas", 1)
    if (
        isinstance(parcelas, bool)
        or not isinstance(parcelas, (int, str))
        or not str(parcelas).isdigit()
        or not 1 <= int(parcelas) <= 120
    ):
        raise DadosInvalidos("Informe entre 1 e 120 parcelas.")
    servicos = dados.get("servicos", [])
    if not isinstance(servicos, list) or any(
        not isinstance(s, str) or s not in SERVICOS for s in servicos
    ):
        raise DadosInvalidos("Selecione os serviços inclusos da lista.")
    observacoes = dados.get("observacoes") or ""
    if len(observacoes) > 4000:
        raise DadosInvalidos("Use até 4000 caracteres nas condições da proposta.")
    return dict(
        fornecedor=nome,
        categoria=categoria,
        valor=valor,
        desconto=desconto,
        taxas=taxas,
        parcelas=int(parcelas),
        servicos_json=json.dumps(sorted(set(servicos))),
        observacoes=observacoes.strip(),
    )
