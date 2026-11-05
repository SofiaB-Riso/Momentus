from secrets import token_urlsafe

from .crud import CrudModel
from .database import db
from .tempo import utcnow


class Convidado(CrudModel, db.Model):
    __tablename__ = "convidados"

    id = db.Column(db.Integer, primary_key=True)
    evento_id = db.Column(
        db.Integer,
        db.ForeignKey("eventos.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    nome = db.Column(db.String(160), nullable=False)
    email = db.Column(db.String(180), nullable=True, default="")
    telefone = db.Column(db.String(40), nullable=True, default="")
    vinculo = db.Column(db.String(100), nullable=True, default="")
    status = db.Column(db.String(20), nullable=False, default="pendente")
    restricoes_alimentares = db.Column(db.Text, nullable=True, default="")
    token_rsvp = db.Column(
        db.String(120), unique=True, nullable=False, default=lambda: token_urlsafe(24)
    )
    criado_em = db.Column(db.DateTime, nullable=False, default=utcnow)

    evento = db.relationship("Evento", back_populates="convidados_rel")
    consentimento = db.relationship(
        "ConsentimentoAlimentar", uselist=False, cascade="all, delete-orphan"
    )
    entrada_espera = db.relationship(
        "EntradaEspera",
        back_populates="convidado",
        uselist=False,
        cascade="all, delete-orphan",
    )

    @property
    def preferencias_seguras(self):
        return (
            self.restricoes_alimentares
            if self.consentimento and self.consentimento.preferencias_sem_saude
            else ""
        )

    @property
    def informacoes_alimentares(self):
        saude = (
            self.consentimento.saude
            if self.consentimento and self.consentimento.vigente
            else ""
        )
        return "; ".join(filter(None, (self.preferencias_seguras, saude)))

    def to_dict(self, incluir_token=True):
        contato = self.email or self.telefone or ""
        dados = {
            "id": str(self.id),
            "nome": self.nome,
            "email": self.email or "",
            "telefone": self.telefone or "",
            "contato": contato,
            "vinculo": self.vinculo or "",
            "status": self.status,
            "restricoes": self.informacoes_alimentares or "",
            "preferencias_alimentares": self.preferencias_seguras or "",
            "informacoes_saude": self.consentimento.saude
            if self.consentimento and self.consentimento.vigente
            else "",
            "consentimento": self.consentimento.to_dict()
            if self.consentimento
            else None,
            "dados_anteriores_pendentes": bool(
                self.restricoes_alimentares and not self.preferencias_seguras
            ),
        }
        if incluir_token:
            dados["token_rsvp"] = self.token_rsvp
        return dados
