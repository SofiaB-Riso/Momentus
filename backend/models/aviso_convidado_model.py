from .crud import CrudModel
from .database import db
from .tempo import utcnow


class AvisoConvidado(CrudModel, db.Model):
    __tablename__ = "avisos_convidado"
    __table_args__ = (
        db.UniqueConstraint("convidado_id", "chave", name="uq_aviso_convidado_chave"),
    )
    id = db.Column(db.Integer, primary_key=True)
    convidado_id = db.Column(
        db.Integer,
        db.ForeignKey("convidados.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    chave = db.Column(db.String(150), nullable=False)
    titulo = db.Column(db.String(180), nullable=False)
    mensagem = db.Column(db.Text, nullable=False)
    criado_em = db.Column(db.DateTime, nullable=False, default=utcnow)
    convidado = db.relationship(
        "Convidado", backref=db.backref("avisos", cascade="all, delete-orphan")
    )

    def to_dict(self):
        return {
            "id": self.id,
            "titulo": self.titulo,
            "mensagem": self.mensagem,
            "criado_em": self.criado_em.isoformat() + "Z",
        }
