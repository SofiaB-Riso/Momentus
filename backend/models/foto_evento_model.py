from .crud import CrudModel
from .database import db
from .tempo import utcnow


class FotoEvento(CrudModel, db.Model):
    __tablename__ = "fotos_evento"

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
    arquivo = db.Column(db.String(255), nullable=False)
    legenda = db.Column(db.String(255), nullable=True, default="")
    criado_em = db.Column(db.DateTime, nullable=False, default=utcnow)

    evento = db.relationship("Evento", back_populates="fotos_rel")

    def to_dict(self):
        return {
            "id": str(self.id),
            "arquivo": self.arquivo,
            "url": f"/uploads/{self.arquivo}",
            "legenda": self.legenda or "",
            "criado_em": self.criado_em.isoformat() + "Z" if self.criado_em else None,
        }
