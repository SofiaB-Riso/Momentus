from models.evento_model import Evento


class ListarEventosService:
    def executar(self):
        eventos = Evento.listar_todos()
        return [evento.to_dict() for evento in eventos]
