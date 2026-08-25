from functools import wraps

from flask import jsonify, session

from models import ColaboradorEvento, Evento, Usuario


def usuario_atual():
    usuario_id = session.get("usuario_id")
    if not usuario_id:
        return None
    return Usuario.query.filter_by(id=usuario_id, ativo=True).first()


def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        usuario = usuario_atual()
        if usuario is None:
            return jsonify({"erro": "Faça login para continuar.", "codigo": "AUTH_REQUIRED"}), 401
        return func(*args, **kwargs)
    return wrapper


def acesso_evento(evento_id, exigir_edicao=False):
    usuario = usuario_atual()
    if usuario is None:
        return None, None

    evento = Evento.buscar_por_id(evento_id)
    if evento is None:
        return usuario, None

    if evento.owner_id == usuario.id:
        return usuario, evento

    colaboracao = ColaboradorEvento.query.filter_by(
        evento_id=evento.id,
        usuario_id=usuario.id,
        status="ativo",
    ).first()
    if colaboracao and (not exigir_edicao or colaboracao.pode_editar):
        return usuario, evento

    return usuario, False
