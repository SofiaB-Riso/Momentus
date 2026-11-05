from .crud import CrudModel
from .database import db
from .tempo import utcnow


class ItemCompartilhado(CrudModel, db.Model):
    __tablename__ = "itens_compartilhados"

    id = db.Column(db.Integer, primary_key=True)
    evento_id = db.Column(
        db.Integer,
        db.ForeignKey("eventos.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    nome = db.Column(db.String(160), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False, default=1)
    responsavel_tipo = db.Column(db.String(30), nullable=True)
    responsavel_id = db.Column(db.Integer, nullable=True)
    responsavel_nome = db.Column(db.String(160), nullable=True, default="")
    criado_em = db.Column(db.DateTime, nullable=False, default=utcnow)

    evento = db.relationship("Evento", back_populates="itens_compartilhados_rel")

    def to_dict(self):
        return {
            "id": str(self.id),
            "nome": self.nome,
            "quantidade": self.quantidade,
            "responsavelTipo": self.responsavel_tipo,
            "responsavelId": str(self.responsavel_id) if self.responsavel_id else None,
            "responsavelNome": self.responsavel_nome or "",
        }
