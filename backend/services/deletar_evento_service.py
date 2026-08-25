from models import Evento, db


class DeletarEventoService:
    def executar(self, evento_id):
        evento = Evento.buscar_por_id(evento_id)
        if evento is None:
            return False
        db.session.delete(evento)
        db.session.commit()
        return True
