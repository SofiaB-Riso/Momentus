from flask import Blueprint, current_app, request
from services.fornecedor_service import (
    BuscarFornecedorService,
    ListarFornecedoresService,
)

from controllers.registro import registrar_controller
from controllers.respostas import responder

fornecedor_controller = Blueprint("fornecedor_controller", __name__)


class FornecedorController:
    """Adaptador HTTP do recurso; regras de negócio ficam nos Services."""

    def listar_fornecedores(self):
        caso = current_app.extensions["momentus"].caso(ListarFornecedoresService)
        return responder(caso.executar(request.args.to_dict()))

    def buscar_fornecedor(self, fornecedor_id):
        caso = current_app.extensions["momentus"].caso(BuscarFornecedorService)
        return responder(caso.executar(fornecedor_id))


registrar_controller(
    fornecedor_controller,
    FornecedorController,
    [
        ("GET", "/fornecedores", "listar_fornecedores"),
        ("GET", "/fornecedores/<int:fornecedor_id>", "buscar_fornecedor"),
    ],
)
