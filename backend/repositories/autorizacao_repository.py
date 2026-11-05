from hashlib import sha256

from models import AutorizacaoConta, ConsentimentoAlimentar, Convidado, Usuario
from models.tempo import utcnow


class AutorizacaoRepository:
    @staticmethod
    def pelo_token(tipo, token):
        if not isinstance(tipo, str):
            return None, None
        model = {"conta": AutorizacaoConta, "convidado": ConsentimentoAlimentar}.get(
            tipo
        )
        if not model or not isinstance(token, str) or not 32 <= len(token) <= 100:
            return None, None
        registro = model.buscar_um(token_hash=sha256(token.encode()).hexdigest())
        if not registro or not registro.expira_em or registro.expira_em < utcnow():
            return None, None
        titular = (
            Usuario.buscar_por_id(registro.usuario_id)
            if tipo == "conta"
            else Convidado.buscar_por_id(registro.convidado_id)
        )
        return registro, titular

    @staticmethod
    def consumir(registro):
        model = type(registro)
        chave = (
            "usuario_id" if isinstance(registro, AutorizacaoConta) else "convidado_id"
        )
        return model.query.filter(
            getattr(model, chave) == getattr(registro, chave),
            model.token_hash == registro.token_hash,
            model.expira_em >= utcnow(),
        ).update({"token_hash": None, "expira_em": None})
