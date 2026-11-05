from models import (
    ColaboradorEvento,
    DespesaEvento,
    FavoritoFornecedor,
    FotoEvento,
    LogEvento,
    Notificacao,
    Usuario,
    db,
)


class UsuarioRepository:
    @staticmethod
    def por_email(email, ativo=None, exceto_id=None):
        consulta = Usuario.query.filter(db.func.lower(Usuario.email) == email.lower())
        if ativo is not None:
            consulta = consulta.filter(Usuario.ativo.is_(ativo))
        if exceto_id is not None:
            consulta = consulta.filter(Usuario.id != exceto_id)
        return consulta.first()

    @staticmethod
    def desvincular_conta(usuario_id):
        usuario = Usuario.buscar_por_id(usuario_id)
        participacoes = ColaboradorEvento.listar(usuario_id=usuario_id)
        for colab in participacoes:
            for log in LogEvento.listar(evento_id=colab.evento_id):
                if log.usuario_id == usuario_id or (
                    log.acao.startswith("colaborador_")
                    and (
                        colab.email in (log.detalhe or "")
                        or colab.nome in (log.detalhe or "")
                    )
                ):
                    log.detalhe = "Registro anonimizado após exclusão da conta."
                    log.usuario_id = None
            for aviso in Notificacao.listar(
                evento_id=colab.evento_id, referencia_id=colab.id
            ):
                if aviso.tipo.startswith(("colaborador-", "convite-")):
                    aviso.mensagem = "A conta de uma pessoa participante foi excluída."
                    aviso.tipo = "conta-excluida"
            for despesa in DespesaEvento.listar(
                evento_id=colab.evento_id, pago_por=usuario.nome
            ):
                despesa.pago_por = "Participante excluído"
            colab.nome = "Participante excluído"
            colab.email = ""
            from secrets import token_urlsafe

            colab.token = token_urlsafe(32)
        for log in LogEvento.listar(usuario_id=usuario_id):
            log.detalhe = "Registro anonimizado após exclusão da conta."
        db.session.flush()
        for model in (ColaboradorEvento, FotoEvento, LogEvento):
            model.query.filter_by(usuario_id=usuario_id).update(
                {"usuario_id": None}, synchronize_session=False
            )
        Notificacao.query.filter_by(usuario_id=usuario_id).delete(
            synchronize_session=False
        )
        FavoritoFornecedor.query.filter_by(usuario_id=usuario_id).delete(
            synchronize_session=False
        )
