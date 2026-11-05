import json
from decimal import Decimal

from .crud import CrudModel
from .database import db
from .tempo import utcnow


class PropostaFornecedor(CrudModel, db.Model):
    __tablename__ = "propostas_fornecedor"
    id = db.Column(db.Integer, primary_key=True)
    evento_id = db.Column(
        db.Integer,
        db.ForeignKey("eventos.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    fornecedor = db.Column(db.String(160), nullable=False)
    categoria = db.Column(db.String(40), nullable=False)
    valor = db.Column(db.Numeric(10, 2), nullable=False)
    desconto = db.Column(db.Numeric(10, 2), nullable=False, default=0)
    taxas = db.Column(db.Numeric(10, 2), nullable=False, default=0)
    parcelas = db.Column(db.Integer, nullable=False, default=1)
    servicos_json = db.Column(db.Text, nullable=False, default="[]")
    observacoes = db.Column(db.Text, nullable=False, default="")
    criado_em = db.Column(db.DateTime, nullable=False, default=utcnow)

    @property
    def total(self):
        return Decimal(self.valor) - Decimal(self.desconto) + Decimal(self.taxas)

    def to_dict(self):
        centavos = int(self.total * 100)
        base, resto = divmod(centavos, self.parcelas)
        return {
            "id": self.id,
            "evento_id": self.evento_id,
            "fornecedor": self.fornecedor,
            "categoria": self.categoria,
            "valor": float(self.valor),
            "desconto": float(self.desconto),
            "taxas": float(self.taxas),
            "total": float(self.total),
            "parcelas": self.parcelas,
            "primeira_parcela": float(Decimal(base + bool(resto)) / 100),
            "servicos": json.loads(self.servicos_json),
            "observacoes": self.observacoes,
        }
