from .crud import CrudModel
from .database import db


class PreferenciasUsuario(CrudModel, db.Model):
    __tablename__ = "preferencias_usuarios"
    usuario_id = db.Column(
        db.Integer, db.ForeignKey("usuarios.id", ondelete="CASCADE"), primary_key=True
    )
    rsvp = db.Column(db.Boolean, nullable=False, default=True)
    lembretes = db.Column(db.Boolean, nullable=False, default=True)

    def to_dict(self):
        return {"rsvp": bool(self.rsvp), "lembretes": bool(self.lembretes)}
