from .crud import CrudModel
from .database import db


class PlanejamentoEvento(CrudModel, db.Model):
    __tablename__ = "planejamento_eventos"
    evento_id = db.Column(
        db.Integer, db.ForeignKey("eventos.id", ondelete="CASCADE"), primary_key=True
    )
    duracao_minutos = db.Column(db.Integer, nullable=False, default=180)
    limite_vagas = db.Column(db.Integer)
    cronograma_ativo = db.Column(db.Boolean, nullable=False, default=False)
    cronograma_gerado_em = db.Column(db.DateTime)

    def to_dict(self):
        return {
            "duracao_minutos": self.duracao_minutos,
            "limite_vagas": self.limite_vagas,
            "cronograma_ativo": self.cronograma_ativo,
            "cronograma_gerado_em": self.cronograma_gerado_em.isoformat() + "Z"
            if self.cronograma_gerado_em
            else None,
        }
