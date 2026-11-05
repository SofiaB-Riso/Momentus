from .crud import CrudModel
from .database import db
from .tempo import utcnow


class DespesaEvento(CrudModel, db.Model):
    __tablename__ = "despesas_evento"

    id = db.Column(db.Integer, primary_key=True)
    evento_id = db.Column(
        db.Integer,
        db.ForeignKey("eventos.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    descricao = db.Column(db.String(200), nullable=False)
    categoria = db.Column(db.String(100), nullable=True, default="geral")
    valor = db.Column(db.Numeric(10, 2), nullable=False, default=0)
    comprovante = db.Column(db.String(255), nullable=True, default="")
    pago_por = db.Column(db.String(160), nullable=True, default="")
    criado_em = db.Column(db.DateTime, nullable=False, default=utcnow)

    evento = db.relationship("Evento", back_populates="despesas_rel")

    def to_dict(self):
        return {
            "id": str(self.id),
            "descricao": self.descricao,
            "categoria": self.categoria or "geral",
            "valor": float(self.valor or 0),
            "comprovante": self.comprovante or "",
            "comprovante_url": f"/uploads/{self.comprovante}"
            if self.comprovante
            else "",
            "pago_por": self.pago_por or "",
            "criado_em": self.criado_em.isoformat() + "Z" if self.criado_em else None,
        }
