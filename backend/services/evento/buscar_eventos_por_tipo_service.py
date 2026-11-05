from application.contratos import BuscaEventosPorTipo
from application.erros import DadosInvalidos
from services.caso_uso import CasoUso
from services.serializacao_evento import serializar_evento
from sqlalchemy.exc import SQLAlchemyError


class BuscarEventosPorTipoService(CasoUso):
    def __init__(self, transacao, usuario_id, repositorio: BuscaEventosPorTipo):
        super().__init__(transacao, usuario_id)
        self.repositorio = repositorio

    def executar(self, params=None):
        try:
            tipo_evento = params.get("tipo_evento")
            eventos = self._preparar(tipo_evento, self.usuario_atual().id)
            return eventos
        except ValueError as erro:
            raise DadosInvalidos(str(erro))
        except SQLAlchemyError:
            self.transacao.reverter()
            raise

    def _preparar(self, tipo_evento, usuario_id):
        if not tipo_evento or not tipo_evento.strip():
            raise ValueError("O parâmetro 'tipo_evento' é obrigatório.")
        eventos = self.repositorio.buscar_por_tipo_evento(
            tipo_evento.strip(), usuario_id
        )
        return [serializar_evento(evento) for evento in eventos]
