from models.evento_model import Evento


class DeletarEventoService:
    def executar(self, evento_id):
        evento = Evento.buscar_por_id(evento_id)

        if evento is None:
            return False

        evento.deletar()
        return True
