from models import AvisoConvidado, Notificacao


def notificar_organizacao(
    evento, tipo, titulo, mensagem, referencia_id=None, exceto=None
):
    destinatarios = {evento.owner_id} | {
        c.usuario_id
        for c in evento.colaboradores_rel
        if c.status == "ativo" and c.usuario_id
    }
    for usuario_id in destinatarios - {exceto}:
        Notificacao(
            usuario_id=usuario_id,
            tipo=tipo,
            titulo=titulo,
            mensagem=mensagem,
            evento_id=evento.id,
            referencia_id=referencia_id,
        ).salvar(confirmar=False)


def avisar_convidados(evento, titulo, mensagem, chave):
    for convidado in evento.convidados_rel:
        if convidado.status != "recusado":
            adicionar_aviso(convidado, titulo, mensagem, chave)


def adicionar_aviso(convidado, titulo, mensagem, chave):
    if not AvisoConvidado.buscar_um(convidado_id=convidado.id, chave=chave):
        AvisoConvidado(
            convidado_id=convidado.id, chave=chave, titulo=titulo, mensagem=mensagem
        ).salvar(confirmar=False)
