from .database import db

class Evento(db.Model):
    __tablename__ = "eventos"

    id = db.Column(db.Integer, primary_key=True)
    nome_evento = db.Column(db.String(120), nullable=False)
    tipo_evento = db.Column(db.String(100), nullable=False)
    data_evento = db.Column(db.Date, nullable=False)
    endereco_evento = db.Column(db.String(255), nullable=True, default="")
    orcamento_evento = db.Column(db.Numeric(10,2), nullable=False, default=0)
    dados_evento = db.Column(db.Text, nullable=True)

    def salvar(self):
       
        db.session.add(self)
        db.session.commit()

    def atualizar(self, nome_evento=None, tipo_evento=None, data_evento=None, endereco_evento=None, orcamento_evento=None, dados_evento=None):
        
        if nome_evento is not None:
            self.nome_evento = nome_evento
        if tipo_evento is not None:
            self.tipo_evento = tipo_evento
        if data_evento is not None:
            self.data_evento = data_evento
        if endereco_evento is not None:
            self.endereco_evento = endereco_evento
        if orcamento_evento is not None:
            self.orcamento_evento = orcamento_evento
        if dados_evento is not None:
            self.dados_evento = dados_evento

        db.session.commit()

    def deletar(self):
        
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def listar_todos():
        
        return Evento.query.order_by(Evento.id.asc()).all()

    @staticmethod
    def buscar_por_id(id):
       
        return Evento.query.get(id)

    def to_dict(self):
        return {
            "id": self.id,
            "nome_evento": self.nome_evento,
            "tipo_evento": self.tipo_evento,
            "data_evento": self.data_evento.isoformat() if self.data_evento else None,
            "endereco_evento": self.endereco_evento,
            "orcamento_evento": float(self.orcamento_evento) if self.orcamento_evento is not None else None,
            "dados_evento": self.dados_evento
        }
