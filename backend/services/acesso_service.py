from models import ColaboradorEvento, Evento, Usuario


def acesso_evento(usuario_id, evento_id, exigir_edicao=False):
    usuario = Usuario.buscar_um(id=usuario_id, ativo=True) if usuario_id else None
    if usuario is None:
        return (None, None)
    evento = Evento.buscar_por_id(evento_id)
    if evento is None:
        return (usuario, None)
    if evento.owner_id == usuario.id:
        return (usuario, evento)
    colaboracao = ColaboradorEvento.buscar_um(
        evento_id=evento.id, usuario_id=usuario.id, status="ativo"
    )
    if colaboracao and (not exigir_edicao or colaboracao.pode_editar):
        return (usuario, evento)
    return (usuario, False)
