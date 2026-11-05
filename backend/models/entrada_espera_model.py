from .crud import CrudModel
from .database import db
from .tempo import utcnow


class EntradaEspera(CrudModel, db.Model):
    __tablename__ = "entradas_espera"
    id = db.Column(db.Integer, primary_key=True)
    evento_id = db.Column(
        db.Integer,
        db.ForeignKey("eventos.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    convidado_id = db.Column(
        db.Integer,
        db.ForeignKey("convidados.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
    )
    solicitado_em = db.Column(db.DateTime, nullable=False, default=utcnow)
    ativo = db.Column(db.Boolean, nullable=False, default=True)
    convidado = db.relationship("Convidado", back_populates="entrada_espera")
