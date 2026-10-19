from models import (
    ColaboradorEvento,
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
    def convites_sem_conta(email):
        return ColaboradorEvento.query.filter(
            db.func.lower(ColaboradorEvento.email) == email.lower(),
            ColaboradorEvento.usuario_id.is_(None),
        ).all()

    @staticmethod
    def desvincular_conta(usuario_id):
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
