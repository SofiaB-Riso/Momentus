from werkzeug.security import check_password_hash, generate_password_hash

from .crud import CrudModel
from .database import db
from .tempo import utcnow


class Usuario(CrudModel, db.Model):
    __tablename__ = "usuarios"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(160), nullable=False)
    email = db.Column(db.String(180), unique=True, nullable=False, index=True)
    telefone = db.Column(db.String(40), nullable=True, default="")
    senha_hash = db.Column(db.String(255), nullable=False)
    tipo = db.Column(
        db.String(30), nullable=False, default="cliente"
    )  # cliente | fornecedor
    ativo = db.Column(db.Boolean, nullable=False, default=True)
    criado_em = db.Column(db.DateTime, nullable=False, default=utcnow)

    eventos = db.relationship(
        "Evento", back_populates="owner", foreign_keys="Evento.owner_id"
    )
    fornecedor = db.relationship(
        "Fornecedor",
        back_populates="usuario",
        uselist=False,
        cascade="all, delete-orphan",
    )
    privacidade = db.relationship(
        "PrivacidadeUsuario", uselist=False, cascade="all, delete-orphan"
    )
    recuperacoes = db.relationship("RecuperacaoSenha", cascade="all, delete-orphan")
    autorizacao_conta = db.relationship(
        "AutorizacaoConta", uselist=False, cascade="all, delete-orphan"
    )
    preferencias = db.relationship(
        "PreferenciasUsuario", uselist=False, cascade="all, delete-orphan"
    )
    requisicoes_despesa = db.relationship(
        "RequisicaoDespesa", cascade="all, delete-orphan"
    )

    def definir_senha(self, senha):
        self.senha_hash = generate_password_hash(senha)

    def conferir_senha(self, senha):
        return check_password_hash(self.senha_hash, senha)

    def to_dict(self, incluir_fornecedor=True):
        dados = {
            "id": self.id,
            "nome": self.nome,
            "email": self.email,
            "telefone": self.telefone or "",
            "tipo": self.tipo,
            "ativo": self.ativo,
            "criado_em": self.criado_em.isoformat() + "Z" if self.criado_em else None,
            "foto_url": "/uploads/" + self.privacidade.foto_arquivo
            if self.privacidade and self.privacidade.foto_arquivo
            else None,
            "autorizacao_conta": self.autorizacao_conta.to_dict()
            if self.autorizacao_conta
            else None,
            "preferencias": self.preferencias.to_dict()
            if self.preferencias
            else {"rsvp": True, "lembretes": True},
        }
        if incluir_fornecedor and self.fornecedor:
            dados["fornecedor"] = self.fornecedor.to_dict(incluir_usuario=False)
        return dados
