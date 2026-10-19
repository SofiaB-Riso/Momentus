import re
import unicodedata
from decimal import ROUND_HALF_UP, Decimal, InvalidOperation


def normalizar_email(valor):
    if not isinstance(valor, str):
        raise ValueError("Informe um e-mail válido.")
    return valor.strip().lower()


def validar_entrada(dados):
    if not isinstance(dados, dict):
        raise ValueError("Envie um objeto JSON válido.")
    textos = {
        "nome",
        "nome_evento",
        "tipo_evento",
        "data_evento",
        "hora_evento",
        "endereco_evento",
        "cidade_evento",
        "estilo_evento",
        "observacoes",
        "status",
        "privacidade_convidados",
        "email",
        "telefone",
        "senha",
        "contato",
        "vinculo",
        "restricoes",
        "restricoes_alimentares",
        "titulo",
        "prazo",
        "descricao",
        "categoria",
        "pago_por",
        "comprovante",
        "chave",
        "endereco",
        "cidade",
        "estilo",
        "responsavelNome",
        "responsavel_nome",
        "responsavelTipo",
    }
    for campo in textos & dados.keys():
        if dados[campo] is not None and not isinstance(dados[campo], str):
            raise ValueError(f"O campo '{campo}' deve ser texto.")
    limites = {
        "nome": 160,
        "nome_evento": 120,
        "tipo_evento": 100,
        "hora_evento": 10,
        "endereco_evento": 255,
        "cidade_evento": 120,
        "estilo_evento": 100,
        "email": 180,
        "telefone": 40,
        "vinculo": 100,
        "titulo": 200,
        "descricao": 200,
        "categoria": 100,
        "pago_por": 160,
        "comprovante": 255,
        "chave": 180,
        "restricoes": 4000,
        "restricoes_alimentares": 4000,
    }
    for campo, limite in limites.items():
        if (
            campo in dados
            and isinstance(dados[campo], str)
            and len(dados[campo]) > limite
        ):
            raise ValueError(f"O campo '{campo}' deve ter até {limite} caracteres.")
    horario = dados.get("hora_evento")
    if (
        horario
        and horario.strip()
        and not re.fullmatch(r"(?:[01][0-9]|2[0-3]):[0-5][0-9]", horario.strip())
    ):
        raise ValueError(
            "Informe um horário válido entre 00:00 e 23:59, no formato HH:MM."
        )
    for campo in ("pode_editar", "feita", "liberar"):
        if campo in dados and not isinstance(dados[campo], bool):
            raise ValueError(f"O campo '{campo}' deve ser verdadeiro ou falso.")
    return dados


def normalizar(valor):
    texto = unicodedata.normalize("NFKD", str(valor or ""))
    return " ".join(
        "".join((c for c in texto if not unicodedata.combining(c))).casefold().split()
    )


def dinheiro(valor):
    try:
        numero = Decimal(str(valor))
        if not numero.is_finite() or numero < 0 or numero > Decimal("99999999.99"):
            raise ValueError()
        return numero.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    except (InvalidOperation, ValueError, TypeError):
        raise ValueError("Informe um valor monetário válido e não negativo.")


def inteiro_positivo(valor):
    try:
        numero = int(str(valor))
        if numero < 1 or numero > 1000000:
            raise ValueError()
        return numero
    except (ValueError, TypeError):
        raise ValueError("Informe uma quantidade inteira entre 1 e 1.000.000.")
