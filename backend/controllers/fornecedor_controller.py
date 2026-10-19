from flask import Blueprint, current_app, request
from services.fornecedor_service import (
    BuscarFornecedorService,
    ListarFornecedoresService,
)

from controllers.respostas import responder

fornecedor_controller = Blueprint("fornecedor_controller", __name__)


@fornecedor_controller.get("/fornecedores")
def listar_fornecedores():
    caso = current_app.extensions["momentus"].caso(ListarFornecedoresService)
    return responder(caso.executar(request.args.to_dict()))


@fornecedor_controller.get("/fornecedores/<int:fornecedor_id>")
def buscar_fornecedor(fornecedor_id):
    caso = current_app.extensions["momentus"].caso(BuscarFornecedorService)
    return responder(caso.executar(fornecedor_id))
