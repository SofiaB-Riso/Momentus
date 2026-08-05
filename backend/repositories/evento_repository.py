from sqlalchemy import text

from models.database import db
from models.evento_model import Evento


class EventoRepository:

    @staticmethod
    def buscar_por_tipo_evento(tipo_evento):
        banco = db.session.get_bind().dialect.name

        if banco == "mysql":
            sql = text("CALL sp_eventos_por_tipo(:tipo_evento)")
            resultado = db.session.execute(sql, {"tipo_evento": tipo_evento})
            linhas = resultado.mappings().all()
            resultado.close()

            return [Evento(**dict(linha)) for linha in linhas]

        # Fallback apenas para facilitar os testes locais com SQLite em sala.
        # No MySQL, a consulta fica na procedure e o CALL fica neste Repository.
        return (
            Evento.query
            .filter(Evento.tipo_evento == tipo_evento)
            .order_by(Evento.nome_evento.asc())
            .all()
        )
