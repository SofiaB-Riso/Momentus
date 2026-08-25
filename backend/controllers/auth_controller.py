from flask import Blueprint, jsonify, request, session
from sqlalchemy import func

from models import ColaboradorEvento, Evento, FavoritoFornecedor, FotoEvento, LogEvento, Notificacao, Usuario, db
from utils.auth import login_required, usuario_atual

auth_controller = Blueprint("auth_controller", __name__)


def _email_normalizado(valor):
    return (valor or "").strip().lower()


def _vincular_convites_pendentes(usuario):
    convites = ColaboradorEvento.query.filter(
        db.func.lower(ColaboradorEvento.email) == usuario.email.lower(),
        ColaboradorEvento.usuario_id.is_(None),
    ).all()
    for convite in convites:
        convite.usuario_id = usuario.id
        ja_existe = Notificacao.query.filter_by(
            usuario_id=usuario.id,
            tipo="convite-colaborador",
            referencia_id=convite.id,
        ).first()
        if not ja_existe:
            db.session.add(Notificacao(
                usuario_id=usuario.id,
                tipo="convite-colaborador",
                titulo="Convite para colaborar",
                mensagem=f"Você foi convidado para colaborar em {convite.evento.nome_evento}.",
                evento_id=convite.evento_id,
                referencia_id=convite.id,
            ))



@auth_controller.post("/auth/cadastro")
def cadastro():
    dados = request.get_json(silent=True) or {}
    nome = (dados.get("nome") or "").strip()
    email = _email_normalizado(dados.get("email"))
    senha = dados.get("senha") or ""
    telefone = (dados.get("telefone") or "").strip()

    if len(nome) < 2:
        return jsonify({"erro": "Informe seu nome completo."}), 400
    if "@" not in email or "." not in email.split("@")[-1]:
        return jsonify({"erro": "Informe um e-mail válido."}), 400
    if len(senha) < 6:
        return jsonify({"erro": "A senha precisa ter pelo menos 6 caracteres."}), 400
    if Usuario.query.filter(func.lower(Usuario.email) == email).first():
        return jsonify({"erro": "Já existe uma conta com este e-mail."}), 409

    usuario = Usuario(nome=nome, email=email, telefone=telefone, tipo="cliente")
    usuario.definir_senha(senha)
    db.session.add(usuario)
    db.session.flush()

    _vincular_convites_pendentes(usuario)
    db.session.commit()
    session.clear()
    session["usuario_id"] = usuario.id
    return jsonify({"usuario": usuario.to_dict()}), 201


@auth_controller.post("/auth/login")
def login():
    dados = request.get_json(silent=True) or {}
    email = _email_normalizado(dados.get("email"))
    senha = dados.get("senha") or ""
    usuario = Usuario.query.filter(func.lower(Usuario.email) == email, Usuario.ativo.is_(True)).first()

    if usuario is None or not usuario.conferir_senha(senha):
        return jsonify({"erro": "E-mail ou senha incorretos."}), 401

    _vincular_convites_pendentes(usuario)
    db.session.commit()
    session.clear()
    session["usuario_id"] = usuario.id
    return jsonify({"usuario": usuario.to_dict()})


@auth_controller.post("/auth/logout")
def logout():
    session.clear()
    return "", 204


@auth_controller.get("/auth/me")
@login_required
def me():
    return jsonify({"usuario": usuario_atual().to_dict()})


@auth_controller.put("/auth/perfil")
@login_required
def atualizar_perfil():
    usuario = usuario_atual()
    dados = request.get_json(silent=True) or {}

    if "nome" in dados and (dados.get("nome") or "").strip():
        usuario.nome = dados["nome"].strip()
    if "telefone" in dados:
        usuario.telefone = (dados.get("telefone") or "").strip()
    if "email" in dados:
        novo_email = _email_normalizado(dados.get("email"))
        if "@" not in novo_email:
            return jsonify({"erro": "Informe um e-mail válido."}), 400
        existe = Usuario.query.filter(func.lower(Usuario.email) == novo_email, Usuario.id != usuario.id).first()
        if existe:
            return jsonify({"erro": "Este e-mail já está em uso."}), 409
        usuario.email = novo_email

    db.session.commit()
    return jsonify({"usuario": usuario.to_dict()})


@auth_controller.delete("/auth/conta")
@login_required
def excluir_conta():
    usuario = usuario_atual()
    # Remove explicitamente referências para funcionar também no SQLite, onde
    # cascatas de FK podem não estar habilitadas por padrão.
    for evento in Evento.query.filter_by(owner_id=usuario.id).all():
        db.session.delete(evento)
    ColaboradorEvento.query.filter_by(usuario_id=usuario.id).update({"usuario_id": None}, synchronize_session=False)
    FotoEvento.query.filter_by(usuario_id=usuario.id).update({"usuario_id": None}, synchronize_session=False)
    LogEvento.query.filter_by(usuario_id=usuario.id).update({"usuario_id": None}, synchronize_session=False)
    Notificacao.query.filter_by(usuario_id=usuario.id).delete(synchronize_session=False)
    FavoritoFornecedor.query.filter_by(usuario_id=usuario.id).delete(synchronize_session=False)
    db.session.delete(usuario)
    db.session.commit()
    session.clear()
    return "", 204
