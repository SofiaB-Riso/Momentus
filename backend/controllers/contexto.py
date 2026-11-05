"""Construção dos casos de uso com a identidade da requisição atual."""

from flask import current_app
from utils.auth import usuario_atual


def obter_caso(classe):
    usuario = usuario_atual()
    return current_app.extensions["momentus"].caso(
        classe, usuario.id if usuario else None
    )
