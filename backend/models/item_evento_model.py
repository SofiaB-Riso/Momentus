from .crud import CrudModel
from .database import db


class ItemEvento(CrudModel, db.Model):
    __tablename__ = "itens_evento"

    id = db.Column(db.Integer, primary_key=True)
    evento_id = db.Column(
        db.Integer,
        db.ForeignKey("eventos.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    produto_id = db.Column(
        db.Integer,
        db.ForeignKey("produtos_fornecedor.id", ondelete="SET NULL"),
        nullable=True,
    )
    chave_externa = db.Column(db.String(180), nullable=True)
    nome = db.Column(db.String(160), nullable=False)
    categoria = db.Column(db.String(100), nullable=True, default="outros")
    preco = db.Column(db.Numeric(10, 2), nullable=False, default=0)
    quantidade = db.Column(db.Integer, nullable=False, default=1)

    evento = db.relationship("Evento", back_populates="itens_evento_rel")
    produto = db.relationship("ProdutoFornecedor")

    def to_dict(self):
        return {
            "id": str(self.id),
            "produtoId": str(self.produto_id)
            if self.produto_id
            else (self.chave_externa or self.nome.lower()),
            "nome": self.nome,
            "categoria": self.categoria or "outros",
            "preco": float(self.preco or 0),
            "qtd": self.quantidade,
        }
