"""Único adaptador entre resultados da aplicação e respostas HTTP."""

import io

from application.contratos import ArquivoGerado, Criado
from application.erros import (
    Conflito,
    DadosInvalidos,
    ErroAplicacao,
    IntegracaoIndisponivel,
    NaoAutenticado,
    NaoEncontrado,
    Proibido,
)
from flask import jsonify, send_file


def responder(resultado):
    if isinstance(resultado, ArquivoGerado):
        return send_file(
            io.BytesIO(resultado.conteudo),
            mimetype=resultado.tipo,
            as_attachment=True,
            download_name=resultado.nome,
        )
    if isinstance(resultado, Criado):
        return jsonify(resultado.dados), 201
    if resultado is None:
        return "", 204
    return jsonify(resultado)


def registrar_erros(app):
    from sqlalchemy.exc import SQLAlchemyError

    codigos = {
        DadosInvalidos: 400,
        NaoEncontrado: 404,
        Proibido: 403,
        NaoAutenticado: 401,
        Conflito: 409,
        IntegracaoIndisponivel: 502,
    }

    @app.errorhandler(ErroAplicacao)
    def erro_aplicacao(erro):
        app.extensions["momentus"].transacao.reverter()
        return jsonify({"erro": str(erro), **erro.detalhes}), codigos.get(
            type(erro), 400
        )

    @app.errorhandler(ValueError)
    def erro_validacao(erro):
        app.extensions["momentus"].transacao.reverter()
        return jsonify({"erro": str(erro)}), 400

    @app.errorhandler(SQLAlchemyError)
    def erro_banco(erro):
        app.extensions["momentus"].transacao.reverter()
        app.logger.exception("Erro na persistência do caso de uso")
        return jsonify({"erro": "Erro ao executar operação no banco de dados."}), 500
