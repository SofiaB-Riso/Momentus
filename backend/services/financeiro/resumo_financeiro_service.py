from decimal import Decimal

from services.financeiro.estrategias_rateio import ESTRATEGIAS


def resumo_financeiro(evento, estrategias=None):
    total = evento.total_despesas_decimal
    orcamento = Decimal(evento.orcamento_evento or 0)
    pessoas = [{"id": "organizador", "nome": evento.owner.nome, "organizador": True}]
    pessoas += [
        {"id": str(c.id), "nome": c.nome, "organizador": False}
        for c in sorted(evento.colaboradores_rel, key=lambda c: c.id)
        if c.status == "ativo"
    ]
    estrategias = ESTRATEGIAS if estrategias is None else estrategias
    estrategia = estrategias[evento.rateio_modo or "auto"]
    valores = estrategia.calcular(total, len(pessoas), evento.rateio_valor_fixo)
    for pessoa, valor in zip(pessoas, valores):
        pessoa["valor"] = float(valor)
    return {
        "orcamento": float(orcamento),
        "total": float(total),
        "restante": float(orcamento - total),
        "percentual": round(float(total / orcamento * 100), 1) if orcamento else 0,
        "estourou_orcamento": bool(orcamento and total > orcamento),
        "rateio": {
            "ativo": evento.rateio_ativo,
            "modo": evento.rateio_modo,
            "valorFixo": float(evento.rateio_valor_fixo or 0),
            "qtdPessoas": len(pessoas),
            "valorPorPessoa": pessoas[0]["valor"],
            "pessoas": pessoas,
            "totalDespesas": float(total),
            "totalArrecadado": round(sum((p["valor"] for p in pessoas)), 2),
        },
    }
