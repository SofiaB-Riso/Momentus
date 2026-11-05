from .crud import CrudModel
from .database import db
from .tempo import utcnow


class RequisicaoDespesa(CrudModel, db.Model):
    __tablename__ = "requisicoes_despesa"
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(
        db.Integer, db.ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False
    )
    evento_id = db.Column(
        db.Integer,
        db.ForeignKey("eventos.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    despesa_id = db.Column(
        db.Integer, db.ForeignKey("despesas_evento.id", ondelete="SET NULL")
    )
    chave = db.Column(db.String(36), nullable=False)
    assinatura = db.Column(db.String(64), nullable=False)
    criado_em = db.Column(db.DateTime, nullable=False, default=utcnow)
    __table_args__ = (
        db.UniqueConstraint(
            "usuario_id", "chave", name="uq_requisicao_despesa_usuario_chave"
        ),
    )
