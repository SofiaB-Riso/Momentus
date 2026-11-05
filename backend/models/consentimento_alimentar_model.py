from .crud import CrudModel
from .database import db


class ConsentimentoAlimentar(CrudModel, db.Model):
    __tablename__ = "consentimentos_alimentares"
    convidado_id = db.Column(
        db.Integer, db.ForeignKey("convidados.id", ondelete="CASCADE"), primary_key=True
    )
    preferencias_sem_saude = db.Column(db.Boolean, nullable=False, default=False)
    faixa_etaria = db.Column(db.String(20), nullable=False, default="nao_informado")
    saude = db.Column(db.Text, nullable=False, default="")
    versao = db.Column(db.String(40))
    autorizado_em = db.Column(db.DateTime)
    revogado_em = db.Column(db.DateTime)
    origem = db.Column(db.String(30), nullable=False, default="")
    responsavel_nome = db.Column(db.String(160), nullable=False, default="")
    responsavel_email = db.Column(db.String(180), nullable=False, default="")
    vinculo = db.Column(db.String(100), nullable=False, default="")
    responsavel_autorizou = db.Column(db.Boolean)
    responsavel_autorizado_em = db.Column(db.DateTime)
    token_hash = db.Column(db.String(64), unique=True)
    expira_em = db.Column(db.DateTime)

    @property
    def vigente(self):
        identidade = (self.faixa_etaria == "adulto" and self.origem == "rsvp") or (
            self.faixa_etaria == "menor"
            and self.origem == "responsavel"
            and self.responsavel_autorizou is True
        )
        return bool(identidade and self.autorizado_em and not self.revogado_em)

    def to_dict(self, incluir_responsavel=False):
        dados = {
            "faixa_etaria": self.faixa_etaria,
            "autorizado": self.vigente,
            "responsavel_autorizou": self.responsavel_autorizou,
            "versao": self.versao,
            "origem": self.origem,
            "autorizado_em": self.autorizado_em.isoformat() + "Z"
            if self.autorizado_em
            else None,
            "revogado_em": self.revogado_em.isoformat() + "Z"
            if self.revogado_em
            else None,
        }
        if incluir_responsavel:
            dados.update(
                responsavel_nome=self.responsavel_nome,
                responsavel_email=self.responsavel_email,
            )
        return dados
