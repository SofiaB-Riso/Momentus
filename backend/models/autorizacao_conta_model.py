from .crud import CrudModel
from .database import db
from .tempo import utcnow


class AutorizacaoConta(CrudModel, db.Model):
    __tablename__ = "autorizacoes_conta"
    usuario_id = db.Column(
        db.Integer, db.ForeignKey("usuarios.id", ondelete="CASCADE"), primary_key=True
    )
    faixa_etaria = db.Column(db.String(20), nullable=False)
    status = db.Column(db.String(20), nullable=False, default="pendente")
    versao = db.Column(db.String(40), nullable=False)
    declarado_em = db.Column(db.DateTime, nullable=False, default=utcnow)
    autorizado_em = db.Column(db.DateTime)
    revogado_em = db.Column(db.DateTime)
    responsavel_nome = db.Column(db.String(160), nullable=False, default="")
    responsavel_email = db.Column(db.String(180), nullable=False, default="")
    vinculo = db.Column(db.String(100), nullable=False, default="")
    token_hash = db.Column(db.String(64), unique=True)
    expira_em = db.Column(db.DateTime)

    def to_dict(self):
        return {
            "faixa_etaria": self.faixa_etaria,
            "status": self.status,
            "versao": self.versao,
            "autorizado_em": self.autorizado_em.isoformat() + "Z"
            if self.autorizado_em
            else None,
            "responsavel_nome": self.responsavel_nome,
            "responsavel_email": self.responsavel_email,
        }
