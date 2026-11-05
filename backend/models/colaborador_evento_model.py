from secrets import token_urlsafe

from .crud import CrudModel
from .database import db
from .tempo import utcnow


class ColaboradorEvento(CrudModel, db.Model):
    __tablename__ = "colaboradores_evento"

    id = db.Column(db.Integer, primary_key=True)
    evento_id = db.Column(
        db.Integer,
        db.ForeignKey("eventos.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    usuario_id = db.Column(
        db.Integer,
        db.ForeignKey("usuarios.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    nome = db.Column(db.String(160), nullable=False)
    email = db.Column(db.String(180), nullable=False)
    status = db.Column(db.String(20), nullable=False, default="pendente")
    token = db.Column(
        db.String(120), unique=True, nullable=False, default=lambda: token_urlsafe(24)
    )
    pode_editar = db.Column(db.Boolean, nullable=False, default=True)
    criado_em = db.Column(db.DateTime, nullable=False, default=utcnow)

    evento = db.relationship("Evento", back_populates="colaboradores_rel")
    usuario = db.relationship("Usuario")

    def to_dict(self):
        return {
            "id": str(self.id),
            "usuario_id": self.usuario_id,
            "nome": self.nome,
            "contato": self.email,
            "email": self.email,
            "status": self.status,
            "token": self.token,
            "pode_editar": self.pode_editar,
        }
