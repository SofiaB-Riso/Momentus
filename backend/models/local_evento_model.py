from .crud import CrudModel
from .database import db


class LocalEvento(CrudModel, db.Model):
    """Orçamentos de espaços comparados pela organização; Google não fornece lotação/preço de aluguel."""

    __tablename__ = "locais_evento"
    __table_args__ = (
        db.UniqueConstraint("evento_id", "chave", name="uq_local_evento_chave"),
    )
    id = db.Column(db.Integer, primary_key=True)
    evento_id = db.Column(
        db.Integer,
        db.ForeignKey("eventos.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    chave = db.Column(db.String(255), nullable=False)
    nome = db.Column(db.String(180), nullable=False)
    endereco = db.Column(db.String(255), nullable=False)
    cidade = db.Column(db.String(120), nullable=False)
    capacidade = db.Column(db.Integer, nullable=False)
    preco = db.Column(db.Numeric(10, 2), nullable=False)
    estilo = db.Column(db.String(100), nullable=False)
    evento = db.relationship(
        "Evento",
        backref=db.backref("locais_rel", cascade="all, delete-orphan", lazy="selectin"),
    )

    def to_dict(self):
        from utils.mapas import links_mapa

        return {
            "id": self.id,
            "nome": self.nome,
            "endereco": self.endereco,
            "cidade": self.cidade,
            "capacidade": self.capacidade,
            "preco": float(self.preco),
            "estilo": self.estilo,
            "mapas": links_mapa(self.endereco, self.cidade),
        }
