from datetime import date, datetime, timedelta

from flask import Blueprint, jsonify, request

from models import Evento, FavoritoFornecedor, Notificacao, TarefaEvento, db
from utils.auth import login_required, usuario_atual

usuario_controller = Blueprint("usuario_controller", __name__)


def _gerar_lembretes(usuario_id):
    hoje = date.today()
    limite = hoje + timedelta(days=2)
    eventos = Evento.query.filter(
        Evento.owner_id == usuario_id,
        Evento.data_evento >= hoje,
        Evento.data_evento <= limite,
    ).all()
    for evento in eventos:
        existe = Notificacao.query.filter_by(
            usuario_id=usuario_id,
            tipo="lembrete-evento",
            evento_id=evento.id,
        ).first()
        if not existe:
            dias = (evento.data_evento - hoje).days
            quando = "hoje" if dias == 0 else ("amanhã" if dias == 1 else "em 2 dias")
            db.session.add(Notificacao(
                usuario_id=usuario_id,
                tipo="lembrete-evento",
                titulo="Evento se aproximando",
                mensagem=f"{evento.nome_evento} acontece {quando}. Confira as pendências.",
                evento_id=evento.id,
            ))

    agora = datetime.now()
    limite_tarefa = agora + timedelta(days=2)
    tarefas = (TarefaEvento.query.join(Evento, TarefaEvento.evento_id == Evento.id)
        .filter(Evento.owner_id == usuario_id, TarefaEvento.feita.is_(False),
                TarefaEvento.prazo.isnot(None), TarefaEvento.prazo >= agora, TarefaEvento.prazo <= limite_tarefa).all())
    for tarefa in tarefas:
        existe = Notificacao.query.filter_by(usuario_id=usuario_id, tipo="lembrete-tarefa", referencia_id=tarefa.id).first()
        if not existe:
            db.session.add(Notificacao(
                usuario_id=usuario_id, tipo="lembrete-tarefa", titulo="Prazo de tarefa próximo",
                mensagem=f"A tarefa “{tarefa.titulo}” está perto do prazo.",
                evento_id=tarefa.evento_id, referencia_id=tarefa.id,
            ))
    db.session.commit()


@usuario_controller.get("/notificacoes")
@login_required
def listar_notificacoes():
    usuario = usuario_atual()
    _gerar_lembretes(usuario.id)
    itens = Notificacao.query.filter_by(usuario_id=usuario.id).order_by(Notificacao.criado_em.desc()).limit(100).all()
    return jsonify([n.to_dict() for n in itens])


@usuario_controller.put("/notificacoes/lidas")
@login_required
def marcar_notificacoes_lidas():
    usuario = usuario_atual()
    Notificacao.query.filter_by(usuario_id=usuario.id, lida=False).update({"lida": True})
    db.session.commit()
    return "", 204


@usuario_controller.get("/favoritos")
@login_required
def listar_favoritos():
    usuario = usuario_atual()
    itens = FavoritoFornecedor.query.filter_by(usuario_id=usuario.id).all()
    return jsonify([f.chave for f in itens])


@usuario_controller.post("/favoritos")
@login_required
def alternar_favorito():
    usuario = usuario_atual()
    dados = request.get_json(silent=True) or {}
    chave = (dados.get("chave") or "").strip()
    if not chave:
        return jsonify({"erro": "Chave do favorito é obrigatória."}), 400
    favorito = FavoritoFornecedor.query.filter_by(usuario_id=usuario.id, chave=chave).first()
    if favorito:
        db.session.delete(favorito)
        ativo = False
    else:
        db.session.add(FavoritoFornecedor(usuario_id=usuario.id, chave=chave))
        ativo = True
    db.session.commit()
    return jsonify({"chave": chave, "favorito": ativo})
