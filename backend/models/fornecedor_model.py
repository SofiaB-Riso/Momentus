from .crud import CrudModel
from .database import db


class Fornecedor(CrudModel, db.Model):
    __tablename__ = "fornecedores"

    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(
        db.Integer,
        db.ForeignKey("usuarios.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
    )
    nome_empresa = db.Column(db.String(180), nullable=False)
    cpf_cnpj = db.Column(db.String(30), unique=True, nullable=False)
    tipo_servico = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text, nullable=True, default="")
    cidade = db.Column(db.String(120), nullable=True, default="")
    endereco = db.Column(db.String(255), nullable=True, default="")
    avaliacao = db.Column(db.Numeric(3, 2), nullable=False, default=5)
    ativo = db.Column(db.Boolean, nullable=False, default=True)

    usuario = db.relationship("Usuario", back_populates="fornecedor")
    produtos = db.relationship(
        "ProdutoFornecedor", back_populates="fornecedor", cascade="all, delete-orphan"
    )

    def to_dict(self, incluir_usuario=True, incluir_produtos=True):
        dados = {
            "id": self.id,
            "usuario_id": self.usuario_id,
            "nome_empresa": self.nome_empresa,
            "cpf_cnpj": self.cpf_cnpj,
            "tipo_servico": self.tipo_servico,
            "descricao": self.descricao or "",
            "cidade": self.cidade or "",
            "endereco": self.endereco or "",
            "avaliacao": float(self.avaliacao or 0),
            "ativo": self.ativo,
        }
        if incluir_usuario and self.usuario:
            dados["usuario"] = {"id": self.usuario.id, "nome": self.usuario.nome}
        if incluir_produtos:
            dados["produtos"] = [
                p.to_dict(incluir_fornecedor=False) for p in self.produtos if p.ativo
            ]
        return dados
