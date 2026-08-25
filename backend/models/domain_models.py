from datetime import datetime
from secrets import token_urlsafe

from werkzeug.security import check_password_hash, generate_password_hash

from .database import db


def utcnow():
    return datetime.utcnow()


class Usuario(db.Model):
    __tablename__ = "usuarios"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(160), nullable=False)
    email = db.Column(db.String(180), unique=True, nullable=False, index=True)
    telefone = db.Column(db.String(40), nullable=True, default="")
    senha_hash = db.Column(db.String(255), nullable=False)
    tipo = db.Column(db.String(30), nullable=False, default="cliente")  # cliente | fornecedor
    ativo = db.Column(db.Boolean, nullable=False, default=True)
    criado_em = db.Column(db.DateTime, nullable=False, default=utcnow)

    eventos = db.relationship("Evento", back_populates="owner", foreign_keys="Evento.owner_id")
    fornecedor = db.relationship("Fornecedor", back_populates="usuario", uselist=False, cascade="all, delete-orphan")

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
            "criado_em": self.criado_em.isoformat() if self.criado_em else None,
        }
        if incluir_fornecedor and self.fornecedor:
            dados["fornecedor"] = self.fornecedor.to_dict(incluir_usuario=False)
        return dados


class Fornecedor(db.Model):
    __tablename__ = "fornecedores"

    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuarios.id", ondelete="CASCADE"), unique=True, nullable=False)
    nome_empresa = db.Column(db.String(180), nullable=False)
    cpf_cnpj = db.Column(db.String(30), unique=True, nullable=False)
    tipo_servico = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text, nullable=True, default="")
    cidade = db.Column(db.String(120), nullable=True, default="")
    endereco = db.Column(db.String(255), nullable=True, default="")
    avaliacao = db.Column(db.Numeric(3, 2), nullable=False, default=5)
    ativo = db.Column(db.Boolean, nullable=False, default=True)

    usuario = db.relationship("Usuario", back_populates="fornecedor")
    produtos = db.relationship("ProdutoFornecedor", back_populates="fornecedor", cascade="all, delete-orphan")

    def to_dict(self, incluir_usuario=True, incluir_produtos=True):
        dados = {
            "id": self.id,
            "usuario_id": self.usuario_id,
            "nome_empresa": self.nome_empresa,
            "cpf_cnpj": self.cpf_cnpj,
            "tipo_servico": self.tipo_servico,
            "descricao": self.descricao or "",
            "cidade": self.cidade or "",
            "endereco": self.endereco or "",
            "avaliacao": float(self.avaliacao or 0),
            "ativo": self.ativo,
        }
        if incluir_usuario and self.usuario:
            dados["usuario"] = self.usuario.to_dict(incluir_fornecedor=False)
        if incluir_produtos:
            dados["produtos"] = [p.to_dict(incluir_fornecedor=False) for p in self.produtos if p.ativo]
        return dados


class ProdutoFornecedor(db.Model):
    __tablename__ = "produtos_fornecedor"

    id = db.Column(db.Integer, primary_key=True)
    fornecedor_id = db.Column(db.Integer, db.ForeignKey("fornecedores.id", ondelete="CASCADE"), nullable=False, index=True)
    nome = db.Column(db.String(160), nullable=False)
    descricao = db.Column(db.Text, nullable=True, default="")
    categoria = db.Column(db.String(100), nullable=False, default="outros")
    preco = db.Column(db.Numeric(10, 2), nullable=False, default=0)
    unidade = db.Column(db.String(60), nullable=True, default="unidade")
    ativo = db.Column(db.Boolean, nullable=False, default=True)

    fornecedor = db.relationship("Fornecedor", back_populates="produtos")

    def to_dict(self, incluir_fornecedor=True):
        dados = {
            "id": self.id,
            "fornecedor_id": self.fornecedor_id,
            "nome": self.nome,
            "descricao": self.descricao or "",
            "categoria": self.categoria,
            "preco": float(self.preco or 0),
            "unidade": self.unidade or "unidade",
            "ativo": self.ativo,
        }
        if incluir_fornecedor and self.fornecedor:
            dados["fornecedor"] = {
                "id": self.fornecedor.id,
                "nome_empresa": self.fornecedor.nome_empresa,
                "tipo_servico": self.fornecedor.tipo_servico,
                "avaliacao": float(self.fornecedor.avaliacao or 0),
            }
        return dados


class Convidado(db.Model):
    __tablename__ = "convidados"

    id = db.Column(db.Integer, primary_key=True)
    evento_id = db.Column(db.Integer, db.ForeignKey("eventos.id", ondelete="CASCADE"), nullable=False, index=True)
    nome = db.Column(db.String(160), nullable=False)
    email = db.Column(db.String(180), nullable=True, default="")
    telefone = db.Column(db.String(40), nullable=True, default="")
    vinculo = db.Column(db.String(100), nullable=True, default="")
    status = db.Column(db.String(20), nullable=False, default="pendente")
    restricoes_alimentares = db.Column(db.Text, nullable=True, default="")
    token_rsvp = db.Column(db.String(120), unique=True, nullable=False, default=lambda: token_urlsafe(24))
    criado_em = db.Column(db.DateTime, nullable=False, default=utcnow)

    evento = db.relationship("Evento", back_populates="convidados_rel")

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
            "restricoes": self.restricoes_alimentares or "",
        }
        if incluir_token:
            dados["token_rsvp"] = self.token_rsvp
        return dados


class ColaboradorEvento(db.Model):
    __tablename__ = "colaboradores_evento"

    id = db.Column(db.Integer, primary_key=True)
    evento_id = db.Column(db.Integer, db.ForeignKey("eventos.id", ondelete="CASCADE"), nullable=False, index=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuarios.id", ondelete="SET NULL"), nullable=True, index=True)
    nome = db.Column(db.String(160), nullable=False)
    email = db.Column(db.String(180), nullable=False)
    status = db.Column(db.String(20), nullable=False, default="pendente")
    token = db.Column(db.String(120), unique=True, nullable=False, default=lambda: token_urlsafe(24))
    pode_editar = db.Column(db.Boolean, nullable=False, default=True)
    criado_em = db.Column(db.DateTime, nullable=False, default=utcnow)

    evento = db.relationship("Evento", back_populates="colaboradores_rel")
    usuario = db.relationship("Usuario")

    def to_dict(self):
        return {
            "id": str(self.id),
            "usuario_id": self.usuario_id,
            "nome": self.nome,
            "contato": self.email,
            "email": self.email,
            "status": self.status,
            "token": self.token,
            "pode_editar": self.pode_editar,
        }


class ItemCompartilhado(db.Model):
    __tablename__ = "itens_compartilhados"

    id = db.Column(db.Integer, primary_key=True)
    evento_id = db.Column(db.Integer, db.ForeignKey("eventos.id", ondelete="CASCADE"), nullable=False, index=True)
    nome = db.Column(db.String(160), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False, default=1)
    responsavel_tipo = db.Column(db.String(30), nullable=True)
    responsavel_id = db.Column(db.Integer, nullable=True)
    responsavel_nome = db.Column(db.String(160), nullable=True, default="")
    criado_em = db.Column(db.DateTime, nullable=False, default=utcnow)

    evento = db.relationship("Evento", back_populates="itens_compartilhados_rel")

    def to_dict(self):
        return {
            "id": str(self.id),
            "nome": self.nome,
            "quantidade": self.quantidade,
            "responsavelTipo": self.responsavel_tipo,
            "responsavelId": str(self.responsavel_id) if self.responsavel_id else None,
            "responsavelNome": self.responsavel_nome or "",
        }


class ItemEvento(db.Model):
    __tablename__ = "itens_evento"

    id = db.Column(db.Integer, primary_key=True)
    evento_id = db.Column(db.Integer, db.ForeignKey("eventos.id", ondelete="CASCADE"), nullable=False, index=True)
    produto_id = db.Column(db.Integer, db.ForeignKey("produtos_fornecedor.id", ondelete="SET NULL"), nullable=True)
    chave_externa = db.Column(db.String(180), nullable=True)
    nome = db.Column(db.String(160), nullable=False)
    categoria = db.Column(db.String(100), nullable=True, default="outros")
    preco = db.Column(db.Numeric(10, 2), nullable=False, default=0)
    quantidade = db.Column(db.Integer, nullable=False, default=1)

    evento = db.relationship("Evento", back_populates="itens_evento_rel")
    produto = db.relationship("ProdutoFornecedor")

    def to_dict(self):
        return {
            "id": str(self.id),
            "produtoId": str(self.produto_id) if self.produto_id else (self.chave_externa or self.nome.lower()),
            "nome": self.nome,
            "categoria": self.categoria or "outros",
            "preco": float(self.preco or 0),
            "qtd": self.quantidade,
        }


class TarefaEvento(db.Model):
    __tablename__ = "tarefas_evento"

    id = db.Column(db.Integer, primary_key=True)
    evento_id = db.Column(db.Integer, db.ForeignKey("eventos.id", ondelete="CASCADE"), nullable=False, index=True)
    titulo = db.Column(db.String(200), nullable=False)
    chave = db.Column(db.String(100), nullable=True)
    feita = db.Column(db.Boolean, nullable=False, default=False)
    prazo = db.Column(db.DateTime, nullable=True)
    ordem = db.Column(db.Integer, nullable=False, default=0)

    evento = db.relationship("Evento", back_populates="tarefas_rel")

    def to_dict(self):
        return {
            "id": str(self.id),
            "titulo": self.titulo,
            "chave": self.chave or "",
            "feita": self.feita,
            "prazo": self.prazo.isoformat() if self.prazo else None,
        }


class DespesaEvento(db.Model):
    __tablename__ = "despesas_evento"

    id = db.Column(db.Integer, primary_key=True)
    evento_id = db.Column(db.Integer, db.ForeignKey("eventos.id", ondelete="CASCADE"), nullable=False, index=True)
    descricao = db.Column(db.String(200), nullable=False)
    categoria = db.Column(db.String(100), nullable=True, default="geral")
    valor = db.Column(db.Numeric(10, 2), nullable=False, default=0)
    comprovante = db.Column(db.String(255), nullable=True, default="")
    pago_por = db.Column(db.String(160), nullable=True, default="")
    criado_em = db.Column(db.DateTime, nullable=False, default=utcnow)

    evento = db.relationship("Evento", back_populates="despesas_rel")

    def to_dict(self):
        return {
            "id": str(self.id),
            "descricao": self.descricao,
            "categoria": self.categoria or "geral",
            "valor": float(self.valor or 0),
            "comprovante": self.comprovante or "",
            "comprovante_url": f"/uploads/{self.comprovante}" if self.comprovante else "",
            "pago_por": self.pago_por or "",
            "criado_em": self.criado_em.isoformat() if self.criado_em else None,
        }


class FotoEvento(db.Model):
    __tablename__ = "fotos_evento"

    id = db.Column(db.Integer, primary_key=True)
    evento_id = db.Column(db.Integer, db.ForeignKey("eventos.id", ondelete="CASCADE"), nullable=False, index=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuarios.id", ondelete="SET NULL"), nullable=True)
    arquivo = db.Column(db.String(255), nullable=False)
    legenda = db.Column(db.String(255), nullable=True, default="")
    criado_em = db.Column(db.DateTime, nullable=False, default=utcnow)

    evento = db.relationship("Evento", back_populates="fotos_rel")

    def to_dict(self):
        return {
            "id": str(self.id),
            "arquivo": self.arquivo,
            "url": f"/uploads/{self.arquivo}",
            "legenda": self.legenda or "",
            "criado_em": self.criado_em.isoformat() if self.criado_em else None,
        }


class Notificacao(db.Model):
    __tablename__ = "notificacoes"

    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False, index=True)
    tipo = db.Column(db.String(60), nullable=False)
    titulo = db.Column(db.String(180), nullable=False)
    mensagem = db.Column(db.Text, nullable=False)
    evento_id = db.Column(db.Integer, db.ForeignKey("eventos.id", ondelete="CASCADE"), nullable=True)
    referencia_id = db.Column(db.Integer, nullable=True)
    lida = db.Column(db.Boolean, nullable=False, default=False)
    criado_em = db.Column(db.DateTime, nullable=False, default=utcnow)

    def to_dict(self):
        return {
            "id": str(self.id),
            "tipo": self.tipo,
            "titulo": self.titulo,
            "mensagem": self.mensagem,
            "eventoId": str(self.evento_id) if self.evento_id else None,
            "referenciaId": str(self.referencia_id) if self.referencia_id else None,
            "lida": self.lida,
            "criadoEm": self.criado_em.isoformat() if self.criado_em else None,
        }


class FavoritoFornecedor(db.Model):
    __tablename__ = "favoritos_fornecedor"
    __table_args__ = (db.UniqueConstraint("usuario_id", "chave", name="uq_favorito_usuario_chave"),)

    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False, index=True)
    chave = db.Column(db.String(180), nullable=False)


class LogEvento(db.Model):
    __tablename__ = "logs_evento"

    id = db.Column(db.Integer, primary_key=True)
    evento_id = db.Column(db.Integer, db.ForeignKey("eventos.id", ondelete="CASCADE"), nullable=False, index=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuarios.id", ondelete="SET NULL"), nullable=True)
    acao = db.Column(db.String(100), nullable=False)
    detalhe = db.Column(db.Text, nullable=True, default="")
    criado_em = db.Column(db.DateTime, nullable=False, default=utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "usuario_id": self.usuario_id,
            "acao": self.acao,
            "detalhe": self.detalhe or "",
            "criado_em": self.criado_em.isoformat() if self.criado_em else None,
        }
