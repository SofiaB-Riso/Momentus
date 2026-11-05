from flask import Blueprint, request
from services.galeria.enviar_foto_service import EnviarFotoService
from services.galeria.remover_foto_service import RemoverFotoService
from utils.auth import login_required

from controllers.contexto import obter_caso
from controllers.registro import registrar_controller
from controllers.respostas import responder

galeria_controller = Blueprint("galeria_controller", __name__)


class GaleriaController:
    """Adaptador HTTP do recurso; regras de negócio ficam nos Services."""

    @login_required
    def remover_foto(self, evento_id, foto_id):
        caso = obter_caso(RemoverFotoService)
        return responder(caso.executar(evento_id, foto_id))

    @login_required
    def enviar_foto(self, evento_id):
        caso = obter_caso(EnviarFotoService)
        return responder(
            caso.executar(
                evento_id, request.files.get("foto"), request.form.get("legenda", "")
            )
        )


registrar_controller(
    galeria_controller,
    GaleriaController,
    [
        ("DELETE", "/eventos/<int:evento_id>/fotos/<int:foto_id>", "remover_foto"),
        ("POST", "/eventos/<int:evento_id>/fotos", "enviar_foto"),
    ],
)
