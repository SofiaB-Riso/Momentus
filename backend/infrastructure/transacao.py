from models.database import db


class TransacaoSQLAlchemy:
    """Uma transação por caso de uso; banco e histórico são confirmados juntos."""

    def sincronizar(self):
        db.session.flush()

    def confirmar(self):
        db.session.commit()

    def reverter(self):
        db.session.rollback()

    def encerrar(self):
        db.session.remove()
