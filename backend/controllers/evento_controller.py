from flask import Blueprint, jsonify, request
from sqlalchemy.exc import SQLAlchemyError

from services.criar_evento_service import CriarEventoService
from services.listar_evento_service import ListarEventosService
from services.buscar_evento_por_id_service import BuscarEventoPorIdService
from services.atualizar_evento_service import AtualizarEventoService
from services.deletar_evento_service import DeletarEventoService
from services.buscar_evento_por_tipo_service import BuscarEventosPorTipoService
from models.database import db

evento_controller = Blueprint("evento_controller", __name__)


@evento_controller.post("/eventos")
def criar_evento():
    try:
        dados = request.get_json() or {}
        service = CriarEventoService()
        evento = service.executar(dados)
        return jsonify(evento), 201

    except ValueError as erro:
        return jsonify({"erro": str(erro)}), 400

    except SQLAlchemyError:
        db.session.rollback()
        return jsonify({"erro": "Erro ao salvar evento no banco de dados."}), 500


@evento_controller.get("/eventos")
def listar_evento():
    service = ListarEventosService()
    eventos = service.executar()
    return jsonify(eventos), 200


@evento_controller.get("/eventos/por-tipo")
def buscar_eventos_por_tipo():
    try:
        tipo_evento = request.args.get("tipo_evento")
        service = BuscarEventosPorTipoService()
        eventos = service.executar(tipo_evento)
        return jsonify(eventos), 200

    except ValueError as erro:
        return jsonify({"erro": str(erro)}), 400

    except SQLAlchemyError:
        db.session.rollback()
        return jsonify({"erro": "Erro ao buscar eventos por tipo."}), 500


@evento_controller.get("/eventos/<int:evento_id>")
def buscar_evento_por_id(evento_id):
    service = BuscarEventoPorIdService()
    evento = service.executar(evento_id)

    if evento is None:
        return jsonify({"erro": "Evento não encontrado."}), 404

    return jsonify(evento), 200


@evento_controller.put("/eventos/<int:evento_id>")
def atualizar_evento(evento_id):
    try:
        dados = request.get_json() or {}
        service = AtualizarEventoService()
        evento = service.executar(evento_id, dados)

        if evento is None:
            return jsonify({"erro": "Evento não encontrado."}), 404

        return jsonify(evento), 200

    except ValueError as erro:
        return jsonify({"erro": str(erro)}), 400

    except SQLAlchemyError:
        db.session.rollback()
        return jsonify({"erro": "Erro ao atualizar evento no banco de dados."}), 500


@evento_controller.delete("/eventos/<int:evento_id>")
def deletar_evento(evento_id):
    try:
        service = DeletarEventoService()
        evento_deletado = service.executar(evento_id)

        if evento_deletado is False:
            return jsonify({"erro": "Evento não encontrado."}), 404

        return "", 204

    except SQLAlchemyError:
        db.session.rollback()
        return jsonify({"erro": "Erro ao deletar evento no banco de dados."}), 500
