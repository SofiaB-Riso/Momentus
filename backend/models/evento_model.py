from .database import db


class Evento(db.Model):
    __tablename__ = "eventos"

    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False, index=True)
    nome_evento = db.Column(db.String(120), nullable=False)
    tipo_evento = db.Column(db.String(100), nullable=False)
    data_evento = db.Column(db.Date, nullable=False)
    hora_evento = db.Column(db.String(10), nullable=True, default="")
    endereco_evento = db.Column(db.String(255), nullable=True, default="")
    cidade_evento = db.Column(db.String(120), nullable=True, default="")
    orcamento_evento = db.Column(db.Numeric(10, 2), nullable=False, default=0)
    convidados_estimados = db.Column(db.Integer, nullable=False, default=0)
    estilo_evento = db.Column(db.String(100), nullable=True, default="")
    observacoes = db.Column(db.Text, nullable=True, default="")
    status = db.Column(db.String(30), nullable=False, default="agendado")
    progresso = db.Column(db.Integer, nullable=False, default=0)
    privacidade_convidados = db.Column(db.String(30), nullable=False, default="organizador")
    rateio_ativo = db.Column(db.Boolean, nullable=False, default=False)
    rateio_modo = db.Column(db.String(20), nullable=False, default="auto")
    rateio_valor_fixo = db.Column(db.Numeric(10, 2), nullable=False, default=0)
    dados_evento = db.Column(db.Text, nullable=True)  # compatibilidade com versões anteriores

    owner = db.relationship("Usuario", back_populates="eventos", foreign_keys=[owner_id])
    convidados_rel = db.relationship("Convidado", back_populates="evento", cascade="all, delete-orphan", lazy="selectin")
    colaboradores_rel = db.relationship("ColaboradorEvento", back_populates="evento", cascade="all, delete-orphan", lazy="selectin")
    itens_compartilhados_rel = db.relationship("ItemCompartilhado", back_populates="evento", cascade="all, delete-orphan", lazy="selectin")
    itens_evento_rel = db.relationship("ItemEvento", back_populates="evento", cascade="all, delete-orphan", lazy="selectin")
    tarefas_rel = db.relationship("TarefaEvento", back_populates="evento", cascade="all, delete-orphan", lazy="selectin")
    despesas_rel = db.relationship("DespesaEvento", back_populates="evento", cascade="all, delete-orphan", lazy="selectin")
    fotos_rel = db.relationship("FotoEvento", back_populates="evento", cascade="all, delete-orphan", lazy="selectin")

    def salvar(self):
        db.session.add(self)
        db.session.commit()

    def atualizar(self, **campos):
        for campo, valor in campos.items():
            if valor is not None and hasattr(self, campo):
                setattr(self, campo, valor)
        db.session.commit()

    def deletar(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def buscar_por_id(id):
        return db.session.get(Evento, id)

    @property
    def total_despesas(self):
        despesas = sum(float(d.valor or 0) for d in self.despesas_rel)
        itens = sum(float(i.preco or 0) * (i.quantidade or 1) for i in self.itens_evento_rel)
        return despesas + itens

    @property
    def confirmados(self):
        return sum(1 for c in self.convidados_rel if c.status == "confirmado")

    def to_dict(self, incluir_relacoes=True):
        dados = {
            "id": self.id,
            "owner_id": self.owner_id,
            "owner": {"id": self.owner.id, "nome": self.owner.nome} if self.owner else None,
            "nome_evento": self.nome_evento,
            "tipo_evento": self.tipo_evento,
            "data_evento": self.data_evento.isoformat() if self.data_evento else None,
            "hora_evento": self.hora_evento or "",
            "endereco_evento": self.endereco_evento or "",
            "cidade_evento": self.cidade_evento or "",
            "orcamento_evento": float(self.orcamento_evento or 0),
            "convidados_estimados": self.convidados_estimados or 0,
            "estilo_evento": self.estilo_evento or "",
            "observacoes": self.observacoes or "",
            "status": self.status,
            "progresso": self.progresso or 0,
            "privacidade_convidados": self.privacidade_convidados,
            "rateio": {
                "ativo": bool(self.rateio_ativo),
                "modo": self.rateio_modo or "auto",
                "valorFixo": float(self.rateio_valor_fixo or 0),
            },
            "total_despesas": self.total_despesas,
            "confirmados": self.confirmados,
            "dados_evento": self.dados_evento,
        }
        if incluir_relacoes:
            dados.update({
                "lista_convidados": [c.to_dict() for c in self.convidados_rel],
                "colaboradores": [c.to_dict() for c in self.colaboradores_rel],
                "itens_compartilhados": [i.to_dict() for i in self.itens_compartilhados_rel],
                "itens_catalogo": [i.to_dict() for i in self.itens_evento_rel],
                "tarefas": [t.to_dict() for t in sorted(self.tarefas_rel, key=lambda x: (x.ordem, x.id))],
                "despesas": [d.to_dict() for d in self.despesas_rel],
                "fotos": [f.to_dict() for f in self.fotos_rel],
            })
        return dados
