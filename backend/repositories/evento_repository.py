from sqlalchemy import text

from models import Evento, db


class EventoRepository:
    @staticmethod
    def buscar_por_tipo_evento(tipo_evento, usuario_id):
        banco = db.session.get_bind().dialect.name
        if banco == "mysql":
            resultado = db.session.execute(
                text("CALL sp_eventos_por_tipo(:tipo_evento, :owner_id)"),
                {"tipo_evento": tipo_evento, "owner_id": usuario_id},
            )
            linhas = resultado.mappings().all()
            resultado.close()
            # Recarrega ORM para incluir relacionamentos e evitar objetos parciais.
            ids = [linha["id"] for linha in linhas]
            if not ids:
                return []
            return Evento.query.filter(Evento.id.in_(ids)).order_by(Evento.nome_evento.asc()).all()

        return (
            Evento.query
            .filter(Evento.owner_id == usuario_id, Evento.tipo_evento == tipo_evento)
            .order_by(Evento.nome_evento.asc())
            .all()
        )
