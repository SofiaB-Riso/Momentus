from .crud import CrudModel
from .database import db
from .tempo import utcnow


class LogEvento(CrudModel, db.Model):
    __tablename__ = "logs_evento"

    id = db.Column(db.Integer, primary_key=True)
    evento_id = db.Column(
        db.Integer,
        db.ForeignKey("eventos.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    usuario_id = db.Column(
        db.Integer, db.ForeignKey("usuarios.id", ondelete="SET NULL"), nullable=True
    )
    acao = db.Column(db.String(100), nullable=False)
    detalhe = db.Column(db.Text, nullable=True, default="")
    criado_em = db.Column(db.DateTime, nullable=False, default=utcnow)
    usuario = db.relationship("Usuario")

    def to_dict(self):
        return {
            "id": self.id,
            "usuario_id": self.usuario_id,
            "autor": self.usuario.nome if self.usuario else "Convidado / sistema",
            "acao": self.acao,
            "detalhe": self.detalhe or "",
            "criado_em": self.criado_em.isoformat() + "Z" if self.criado_em else None,
        }
