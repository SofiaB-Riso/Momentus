from flask import Blueprint, current_app
from utils.auth import login_required, usuario_atual

from controllers.respostas import responder

relatorios_controller = Blueprint("relatorios_controller", __name__)


@relatorios_controller.get("/eventos/<int:evento_id>/relatorio.pdf")
@login_required
def relatorio_pdf(evento_id):
    caso = current_app.extensions["momentus"].relatorio("pdf", usuario_atual().id)
    return responder(caso.executar(evento_id))


@relatorios_controller.get("/eventos/<int:evento_id>/relatorio.xlsx")
@login_required
def relatorio_xlsx(evento_id):
    caso = current_app.extensions["momentus"].relatorio("xlsx", usuario_atual().id)
    return responder(caso.executar(evento_id))
