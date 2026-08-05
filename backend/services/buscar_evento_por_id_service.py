from models.evento_model import Evento


class BuscarEventoPorIdService:
    def executar(self, evento_id):
        evento = Evento.buscar_por_id(evento_id)

        if evento is None:
            return None

        return evento.to_dict()
