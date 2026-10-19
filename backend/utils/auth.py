from functools import wraps
from hashlib import sha256
from hmac import compare_digest

from application.erros import NaoAutenticado
from flask import jsonify, session
from models import Usuario


def _identidade_sessao(usuario):
    """Vincula o ID ao cadastro, sem colocar o hash de senha no cookie."""
    identidade = f"{usuario.id}:{usuario.criado_em.isoformat()}:{usuario.senha_hash}"
    return sha256(identidade.encode("utf-8")).hexdigest()


def iniciar_sessao(usuario_id):
    usuario = Usuario.buscar_um(id=usuario_id, ativo=True)
    session.clear()
    if usuario is None:
        raise NaoAutenticado("Faça login para continuar.")
    session["usuario_id"] = usuario.id
    session["usuario_identidade"] = _identidade_sessao(usuario)


def usuario_atual():
    usuario_id = session.get("usuario_id")
    if usuario_id is None:
        return None
    identidade = session.get("usuario_identidade")
    if type(usuario_id) is not int or not isinstance(identidade, str):
        session.clear()
        return None
    usuario = Usuario.buscar_um(id=usuario_id, ativo=True)
    if usuario is None or not compare_digest(
        identidade.encode("utf-8"), _identidade_sessao(usuario).encode("ascii")
    ):
        session.clear()
        return None
    return usuario


def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if usuario_atual() is None:
            return jsonify(
                {"erro": "Faça login para continuar.", "codigo": "AUTH_REQUIRED"}
            ), 401
        return func(*args, **kwargs)

    return wrapper
