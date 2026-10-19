from flask import Blueprint, Response, current_app, request
from services.catalogo_service import (
    CatalogoPaginadoService,
    FornecedoresPertoService,
    FotoCatalogoService,
)

from controllers.respostas import responder

catalogo_controller = Blueprint("catalogo_controller", __name__)


@catalogo_controller.get("/catalogo/perto")
def fornecedores_perto():
    classe = (
        CatalogoPaginadoService
        if request.args.get("paginado") == "1"
        else FornecedoresPertoService
    )
    caso = current_app.extensions["momentus"].caso(classe)
    return responder(caso.executar(request.args.to_dict()))


@catalogo_controller.get("/catalogo/foto")
def foto_catalogo():
    caso = current_app.extensions["momentus"].caso(FotoCatalogoService)
    conteudo, tipo = caso.executar(request.args.get("token", ""))
    return Response(
        conteudo, mimetype=tipo, headers={"Cache-Control": "private, max-age=900"}
    )
