import hashlib
import json
import time

from flask import Blueprint, Response, current_app, stream_with_context
from services.atualizacoes_service import AtualizacoesService
from utils.auth import login_required, usuario_atual

planejamento_controller = Blueprint("planejamento_controller", __name__)


def _fluxo(obter_dados, transacao):
    intervalo = current_app.config.get("LIVE_INTERVAL", 2)
    iteracoes = current_app.config.get("LIVE_ITERATIONS", 15)

    @stream_with_context
    def gerar():
        anterior = None
        yield "retry: 3000\n\n"
        for _ in range(iteracoes):
            try:
                dados = obter_dados()
                if dados is None:
                    yield "event: encerrado\ndata: {}\n\n"
                    return
                revisao = hashlib.sha256(
                    json.dumps(dados, sort_keys=True, ensure_ascii=False).encode()
                ).hexdigest()
            finally:
                transacao.encerrar()
            if revisao != anterior:
                yield (
                    "event: alteracao\ndata: "
                    + json.dumps({"revisao": revisao})
                    + "\n\n"
                )
                anterior = revisao
            else:
                yield ": conectado\n\n"
            time.sleep(intervalo)

    return Response(
        gerar(),
        mimetype="text/event-stream",
        headers={"Cache-Control": "no-cache, no-store", "X-Accel-Buffering": "no"},
    )


@planejamento_controller.get("/eventos/<int:evento_id>/atualizacoes")
@login_required
def acompanhar_evento(evento_id):
    contexto = current_app.extensions["momentus"]
    caso = contexto.caso(AtualizacoesService, usuario_atual().id)
    caso.validar_evento(evento_id)
    return _fluxo(lambda: caso.evento(evento_id), contexto.transacao)


@planejamento_controller.get("/rsvp/<token>/atualizacoes")
def acompanhar_rsvp(token):
    contexto = current_app.extensions["momentus"]
    caso = contexto.caso(AtualizacoesService)
    caso.validar_rsvp(token)
    return _fluxo(lambda: caso.rsvp(token), contexto.transacao)
