from .crud import CrudModel
from .database import db


class FavoritoFornecedor(CrudModel, db.Model):
    __tablename__ = "favoritos_fornecedor"
    __table_args__ = (
        db.UniqueConstraint("usuario_id", "chave", name="uq_favorito_usuario_chave"),
    )

    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(
        db.Integer,
        db.ForeignKey("usuarios.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    chave = db.Column(db.String(180), nullable=False)
