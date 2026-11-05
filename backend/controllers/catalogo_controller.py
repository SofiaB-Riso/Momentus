from flask import Blueprint, Response, current_app, request
from services.catalogo_service import (
    CatalogoPaginadoService,
    FornecedoresPertoService,
    FotoCatalogoService,
)

from controllers.registro import registrar_controller
from controllers.respostas import responder

catalogo_controller = Blueprint("catalogo_controller", __name__)


class CatalogoController:
    """Adaptador HTTP do recurso; regras de negócio ficam nos Services."""

    def fornecedores_perto(self):
        classe = (
            CatalogoPaginadoService
            if request.args.get("paginado") == "1"
            else FornecedoresPertoService
        )
        caso = current_app.extensions["momentus"].caso(classe)
        return responder(caso.executar(request.args.to_dict()))

    def foto_catalogo(self):
        caso = current_app.extensions["momentus"].caso(FotoCatalogoService)
        conteudo, tipo = caso.executar(request.args.get("token", ""))
        return Response(
            conteudo, mimetype=tipo, headers={"Cache-Control": "private, max-age=900"}
        )


registrar_controller(
    catalogo_controller,
    CatalogoController,
    [
        ("GET", "/catalogo/perto", "fornecedores_perto"),
        ("GET", "/catalogo/foto", "foto_catalogo"),
    ],
)
