from .crud import CrudModel
from .database import db


class ProdutoFornecedor(CrudModel, db.Model):
    __tablename__ = "produtos_fornecedor"

    id = db.Column(db.Integer, primary_key=True)
    fornecedor_id = db.Column(
        db.Integer,
        db.ForeignKey("fornecedores.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    nome = db.Column(db.String(160), nullable=False)
    descricao = db.Column(db.Text, nullable=True, default="")
    categoria = db.Column(db.String(100), nullable=False, default="outros")
    preco = db.Column(db.Numeric(10, 2), nullable=False, default=0)
    unidade = db.Column(db.String(60), nullable=True, default="unidade")
    ativo = db.Column(db.Boolean, nullable=False, default=True)

    fornecedor = db.relationship("Fornecedor", back_populates="produtos")

    def to_dict(self, incluir_fornecedor=True):
        dados = {
            "id": self.id,
            "fornecedor_id": self.fornecedor_id,
            "nome": self.nome,
            "descricao": self.descricao or "",
            "categoria": self.categoria,
            "preco": float(self.preco or 0),
            "unidade": self.unidade or "unidade",
            "ativo": self.ativo,
        }
        if incluir_fornecedor and self.fornecedor:
            dados["fornecedor"] = {
                "id": self.fornecedor.id,
                "nome_empresa": self.fornecedor.nome_empresa,
                "tipo_servico": self.fornecedor.tipo_servico,
                "avaliacao": float(self.fornecedor.avaliacao or 0),
            }
        return dados
