import hashlib
import json
import time

from flask import Blueprint, Response, current_app, stream_with_context
from services.convidados.consultar_atualizacao_rsvp_service import (
    ConsultarAtualizacaoRsvpService,
)
from services.evento.consultar_atualizacao_evento_service import (
    ConsultarAtualizacaoEventoService,
)
from utils.auth import login_required, usuario_atual

from controllers.registro import registrar_controller

planejamento_controller = Blueprint("planejamento_controller", __name__)


class PlanejamentoController:
    """Adaptador HTTP do recurso; regras de negócio ficam nos Services."""

    def _fluxo(self, obter_dados, transacao):
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

    @login_required
    def acompanhar_evento(self, evento_id):
        contexto = current_app.extensions["momentus"]
        caso = contexto.caso(ConsultarAtualizacaoEventoService, usuario_atual().id)
        caso.validar(evento_id)
        return self._fluxo(lambda: caso.executar(evento_id), contexto.transacao)

    def acompanhar_rsvp(self, token):
        contexto = current_app.extensions["momentus"]
        caso = contexto.caso(ConsultarAtualizacaoRsvpService)
        caso.validar(token)
        return self._fluxo(lambda: caso.executar(token), contexto.transacao)


registrar_controller(
    planejamento_controller,
    PlanejamentoController,
    [
        ("GET", "/eventos/<int:evento_id>/atualizacoes", "acompanhar_evento"),
        ("GET", "/rsvp/<token>/atualizacoes", "acompanhar_rsvp"),
    ],
)
