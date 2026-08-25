from flask import Blueprint, jsonify, request
from sqlalchemy.exc import SQLAlchemyError

from models import LogEvento, Notificacao, db
from services.atualizar_evento_service import AtualizarEventoService
from services.buscar_evento_por_id_service import BuscarEventoPorIdService
from services.buscar_evento_por_tipo_service import BuscarEventosPorTipoService
from services.criar_evento_service import CriarEventoService
from services.deletar_evento_service import DeletarEventoService
from services.listar_evento_service import ListarEventosService
from utils.auth import acesso_evento, login_required, usuario_atual

evento_controller = Blueprint("evento_controller", __name__)


def _erro_acesso(evento):
    if evento is None:
        return jsonify({"erro": "Evento não encontrado."}), 404
    if evento is False:
        return jsonify({"erro": "Você não tem acesso a este evento."}), 403
    return None


def _registrar_log(evento_id, usuario_id, acao, detalhe=""):
    db.session.add(LogEvento(evento_id=evento_id, usuario_id=usuario_id, acao=acao, detalhe=detalhe))


@evento_controller.post("/eventos")
@login_required
def criar_evento():
    try:
        usuario = usuario_atual()
        evento = CriarEventoService().executar(request.get_json(silent=True) or {}, usuario.id)
        _registrar_log(evento["id"], usuario.id, "evento_criado", evento["nome_evento"])
        db.session.commit()
        return jsonify(evento), 201
    except ValueError as erro:
        db.session.rollback()
        return jsonify({"erro": str(erro)}), 400
    except SQLAlchemyError:
        db.session.rollback()
        return jsonify({"erro": "Erro ao salvar evento no banco de dados."}), 500


@evento_controller.get("/eventos")
@login_required
def listar_eventos():
    return jsonify(ListarEventosService().executar(usuario_atual().id))


@evento_controller.get("/eventos/por-tipo")
@login_required
def buscar_eventos_por_tipo():
    try:
        tipo_evento = request.args.get("tipo_evento")
        eventos = BuscarEventosPorTipoService().executar(tipo_evento, usuario_atual().id)
        return jsonify(eventos)
    except ValueError as erro:
        return jsonify({"erro": str(erro)}), 400
    except SQLAlchemyError:
        db.session.rollback()
        return jsonify({"erro": "Erro ao buscar eventos por tipo."}), 500


@evento_controller.get("/eventos/<int:evento_id>")
@login_required
def buscar_evento_por_id(evento_id):
    usuario, evento = acesso_evento(evento_id)
    erro = _erro_acesso(evento)
    if erro:
        return erro
    dados = BuscarEventoPorIdService().executar(evento_id)
    if evento.owner_id == usuario.id:
        dados["permissao"] = "dono"
        dados["pode_editar"] = True
    else:
        colab = next((c for c in evento.colaboradores_rel if c.usuario_id == usuario.id and c.status == "ativo"), None)
        dados["permissao"] = "colaborador"
        dados["pode_editar"] = bool(colab and colab.pode_editar)
    return jsonify(dados)


@evento_controller.put("/eventos/<int:evento_id>")
@login_required
def atualizar_evento(evento_id):
    usuario, evento = acesso_evento(evento_id, exigir_edicao=True)
    erro = _erro_acesso(evento)
    if erro:
        return erro
    try:
        dados = request.get_json(silent=True) or {}
        antes = {
            "data": evento.data_evento.isoformat() if evento.data_evento else "",
            "hora": evento.hora_evento or "",
            "local": evento.endereco_evento or "",
        }
        atualizado = AtualizarEventoService().executar(evento_id, dados)
        mudancas = []
        if atualizado.get("data_evento", "") != antes["data"]: mudancas.append("data")
        if atualizado.get("hora_evento", "") != antes["hora"]: mudancas.append("horário")
        if atualizado.get("endereco_evento", "") != antes["local"]: mudancas.append("local")
        if mudancas:
            for colab in evento.colaboradores_rel:
                if colab.status == "ativo" and colab.usuario_id and colab.usuario_id != usuario.id:
                    db.session.add(Notificacao(
                        usuario_id=colab.usuario_id, tipo="evento-alterado", titulo="Evento atualizado",
                        mensagem=f"{evento.nome_evento}: houve alteração de {', '.join(mudancas)}.", evento_id=evento.id,
                    ))
        _registrar_log(evento_id, usuario.id, "evento_atualizado", ", ".join(mudancas) if mudancas else "dados gerais")
        db.session.commit()
        return jsonify(atualizado)
    except ValueError as erro_valor:
        db.session.rollback()
        return jsonify({"erro": str(erro_valor)}), 400
    except SQLAlchemyError:
        db.session.rollback()
        return jsonify({"erro": "Erro ao atualizar evento no banco de dados."}), 500


@evento_controller.delete("/eventos/<int:evento_id>")
@login_required
def deletar_evento(evento_id):
    usuario, evento = acesso_evento(evento_id)
    erro = _erro_acesso(evento)
    if erro:
        return erro
    if evento.owner_id != usuario.id:
        return jsonify({"erro": "Somente a pessoa dona do evento pode excluí-lo."}), 403
    try:
        DeletarEventoService().executar(evento_id)
        return "", 204
    except SQLAlchemyError:
        db.session.rollback()
        return jsonify({"erro": "Erro ao deletar evento do banco de dados."}), 500
