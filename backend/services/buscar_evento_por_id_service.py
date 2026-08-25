from models import Evento


class BuscarEventoPorIdService:
    def executar(self, evento_id):
        evento = Evento.buscar_por_id(evento_id)
        return evento.to_dict() if evento else None
