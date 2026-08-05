from repositories.evento_repository import EventoRepository


class BuscarEventosPorTipoService:
    def executar(self, tipo_evento):
        if not tipo_evento or not tipo_evento.strip():
            raise ValueError("O parâmetro 'tipo_evento' é obrigatório.")

        eventos = EventoRepository.buscar_por_tipo_evento(tipo_evento.strip())
        return [evento.to_dict() for evento in eventos]
