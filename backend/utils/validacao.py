import json
import re
import unicodedata
from decimal import ROUND_HALF_UP, Decimal, InvalidOperation


def normalizar_email(valor):
    if not isinstance(valor, str):
        raise ValueError("Informe um e-mail válido.")
    email = valor.strip().lower()
    if len(email) > 180 or not re.fullmatch(r"[^\s@]+@[^\s@.]+(?:\.[^\s@.]+)+", email):
        raise ValueError("Informe um e-mail válido.")
    return email


def validar_nome(valor):
    if not isinstance(valor, str) or not 2 <= len(valor.strip()) <= 160:
        raise ValueError("Informe um nome entre 2 e 160 caracteres.")
    return valor.strip()


def validar_telefone(valor):
    if valor is not None and not isinstance(valor, str):
        raise ValueError("Informe o telefone como texto.")
    telefone = (valor or "").strip()
    if len(telefone) > 40 or (telefone and not re.fullmatch(r"\+?[0-9]+", telefone)):
        raise ValueError("Use apenas números no telefone, com + somente no início.")
    return telefone


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
        "saude",
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
        "responsavel_email",
        "responsavelTipo",
        "faixa_etaria",
        "tipo",
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
        "saude": 4000,
        "senha": 256,
        "observacoes": 10000,
        "contato": 180,
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
    for campo in (
        "pode_editar",
        "feita",
        "liberar",
        "preferencias_sem_saude",
        "autorizar_saude",
        "revogar_saude",
        "declaracao_idade",
        "declaracao_responsavel",
        "autorizar_conta",
    ):
        if campo in dados and not isinstance(dados[campo], bool):
            raise ValueError(f"O campo '{campo}' deve ser verdadeiro ou falso.")
    for campo, limite in (("convidados_estimados", 1000000), ("progresso", 100)):
        if campo in dados and dados[campo] is not None:
            if isinstance(dados[campo], bool) or not re.fullmatch(
                r"[0-9]+", str(dados[campo])
            ):
                raise ValueError(f"O campo '{campo}' deve ser um número inteiro.")
            if int(dados[campo]) > limite:
                raise ValueError(f"O campo '{campo}' deve estar entre 0 e {limite}.")
    for campo in ("nome_evento", "tipo_evento", "data_evento"):
        if campo in dados and not (dados[campo] or "").strip():
            raise ValueError(f"O campo '{campo}' não pode ficar vazio.")
    if "dados_evento" in dados and dados["dados_evento"] is not None:
        valor = dados["dados_evento"]
        if not isinstance(valor, str) or len(valor) > 20000:
            raise ValueError(
                "Os dados extras do evento devem ser JSON em texto com até 20000 caracteres."
            )
        try:
            json.loads(valor)
        except (ValueError, TypeError):
            raise ValueError(
                "Os dados extras do evento devem conter JSON válido."
            ) from None
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
