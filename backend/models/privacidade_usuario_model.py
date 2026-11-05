from .crud import CrudModel
from .database import db


class PrivacidadeUsuario(CrudModel, db.Model):
    __tablename__ = "privacidade_usuarios"

    usuario_id = db.Column(
        db.Integer, db.ForeignKey("usuarios.id", ondelete="CASCADE"), primary_key=True
    )
    foto_arquivo = db.Column(db.String(255), nullable=True)
    termos_versao = db.Column(db.String(40), nullable=True)
    aceito_em = db.Column(db.DateTime, nullable=True)

    def to_dict(self):
        return {
            "versao": self.termos_versao,
            "aceito_em": self.aceito_em.isoformat() + "Z" if self.aceito_em else None,
        }
