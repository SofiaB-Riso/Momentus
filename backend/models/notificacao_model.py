from .crud import CrudModel
from .database import db
from .tempo import utcnow


class Notificacao(CrudModel, db.Model):
    __tablename__ = "notificacoes"

    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(
        db.Integer,
        db.ForeignKey("usuarios.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    tipo = db.Column(db.String(60), nullable=False)
    titulo = db.Column(db.String(180), nullable=False)
    mensagem = db.Column(db.Text, nullable=False)
    evento_id = db.Column(
        db.Integer, db.ForeignKey("eventos.id", ondelete="CASCADE"), nullable=True
    )
    referencia_id = db.Column(db.Integer, nullable=True)
    lida = db.Column(db.Boolean, nullable=False, default=False)
    criado_em = db.Column(db.DateTime, nullable=False, default=utcnow)

    def to_dict(self):
        return {
            "id": str(self.id),
            "tipo": self.tipo,
            "titulo": self.titulo,
            "mensagem": self.mensagem,
            "eventoId": str(self.evento_id) if self.evento_id else None,
            "referenciaId": str(self.referencia_id) if self.referencia_id else None,
            "lida": self.lida,
            "criadoEm": self.criado_em.isoformat() + "Z" if self.criado_em else None,
        }
