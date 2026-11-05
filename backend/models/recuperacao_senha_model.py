from .crud import CrudModel
from .database import db
from .tempo import utcnow


class RecuperacaoSenha(CrudModel, db.Model):
    __tablename__ = "recuperacoes_senha"

    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(
        db.Integer,
        db.ForeignKey("usuarios.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    token_hash = db.Column(db.String(64), nullable=False, unique=True)
    email = db.Column(db.String(180), nullable=False)
    criado_em = db.Column(db.DateTime, nullable=False, default=utcnow)
    expira_em = db.Column(db.DateTime, nullable=False)
    usado_em = db.Column(db.DateTime, nullable=True)
