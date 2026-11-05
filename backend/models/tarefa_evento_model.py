from .crud import CrudModel
from .database import db


class TarefaEvento(CrudModel, db.Model):
    __tablename__ = "tarefas_evento"

    id = db.Column(db.Integer, primary_key=True)
    evento_id = db.Column(
        db.Integer,
        db.ForeignKey("eventos.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    titulo = db.Column(db.String(200), nullable=False)
    chave = db.Column(db.String(100), nullable=True)
    feita = db.Column(db.Boolean, nullable=False, default=False)
    prazo = db.Column(db.DateTime, nullable=True)
    ordem = db.Column(db.Integer, nullable=False, default=0)

    evento = db.relationship("Evento", back_populates="tarefas_rel")

    def to_dict(self):
        return {
            "id": str(self.id),
            "titulo": self.titulo,
            "chave": self.chave or "",
            "feita": self.feita,
            "prazo": self.prazo.isoformat() if self.prazo else None,
        }
