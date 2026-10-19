from models import Notificacao
from repositories.usuario_repository import UsuarioRepository


def _vincular_convites_pendentes(usuario):
    convites = UsuarioRepository.convites_sem_conta(usuario.email)
    for convite in convites:
        convite.usuario_id = usuario.id
        ja_existe = Notificacao.buscar_um(
            usuario_id=usuario.id, tipo="convite-colaborador", referencia_id=convite.id
        )
        if not ja_existe:
            Notificacao(
                usuario_id=usuario.id,
                tipo="convite-colaborador",
                titulo="Convite para colaborar",
                mensagem=f"Você foi convidado para colaborar em {convite.evento.nome_evento}.",
                evento_id=convite.evento_id,
                referencia_id=convite.id,
            ).salvar(confirmar=False)
