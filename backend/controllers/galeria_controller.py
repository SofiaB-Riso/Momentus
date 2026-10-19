from flask import Blueprint, request
from services.galeria.enviar_foto_service import EnviarFotoService
from services.galeria.remover_foto_service import RemoverFotoService
from utils.auth import login_required

from controllers.contexto import obter_caso
from controllers.respostas import responder

galeria_controller = Blueprint("galeria_controller", __name__)


@galeria_controller.delete("/eventos/<int:evento_id>/fotos/<int:foto_id>")
@login_required
def remover_foto(evento_id, foto_id):
    caso = obter_caso(RemoverFotoService)
    return responder(caso.executar(evento_id, foto_id))


@galeria_controller.post("/eventos/<int:evento_id>/fotos")
@login_required
def enviar_foto(evento_id):
    caso = obter_caso(EnviarFotoService)
    return responder(
        caso.executar(
            evento_id, request.files.get("foto"), request.form.get("legenda", "")
        )
    )
