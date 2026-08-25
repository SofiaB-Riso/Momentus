from repositories.evento_repository import EventoRepository


class BuscarEventosPorTipoService:
    def executar(self, tipo_evento, usuario_id):
        if not tipo_evento or not tipo_evento.strip():
            raise ValueError("O parâmetro 'tipo_evento' é obrigatório.")
        eventos = EventoRepository.buscar_por_tipo_evento(tipo_evento.strip(), usuario_id)
        return [evento.to_dict() for evento in eventos]
