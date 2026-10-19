from datetime import datetime, timedelta

from models import ColaboradorEvento, Evento, LogEvento, TarefaEvento, db
from sqlalchemy import or_


class ConsultaEventoRepository:
    @staticmethod
    def acessiveis(usuario_id):
        return (
            Evento.query.outerjoin(
                ColaboradorEvento,
                (ColaboradorEvento.evento_id == Evento.id)
                & (ColaboradorEvento.usuario_id == usuario_id)
                & (ColaboradorEvento.status == "ativo"),
            )
            .filter(
                or_(Evento.owner_id == usuario_id, ColaboradorEvento.id.isnot(None))
            )
            .order_by(Evento.data_evento.asc(), Evento.id.asc())
            .distinct()
            .all()
        )

    @staticmethod
    def revisao(evento_id):
        return (
            db.session.query(db.func.max(LogEvento.id))
            .filter_by(evento_id=evento_id)
            .scalar()
            or 0
        )

    @staticmethod
    def ultimo_log(evento_id):
        return (
            LogEvento.query.filter_by(evento_id=evento_id)
            .order_by(LogEvento.id.desc())
            .first()
        )

    @staticmethod
    def historico(evento_id):
        return (
            LogEvento.query.filter_by(evento_id=evento_id)
            .order_by(LogEvento.criado_em.desc(), LogEvento.id.desc())
            .limit(100)
            .all()
        )

    @staticmethod
    def bloquear(evento_id, renovar=True):
        # No-op UPDATE serializa alterações no evento também no SQLite.
        db.session.execute(
            db.update(Evento)
            .where(Evento.id == evento_id)
            .values(progresso=Evento.progresso)
        )
        if renovar:
            db.session.expire_all()

    @staticmethod
    def para_lembretes(hoje, usuario_id=None, evento_id=None):
        consulta = Evento.query.filter(
            Evento.data_evento >= hoje,
            or_(
                Evento.data_evento <= hoje + timedelta(days=2),
                Evento.id.in_(
                    db.select(TarefaEvento.evento_id).where(
                        TarefaEvento.feita.is_(False),
                        TarefaEvento.prazo <= datetime.now() + timedelta(days=2),
                    )
                ),
            ),
            Evento.status.notin_(["cancelado", "concluido"]),
        )
        if evento_id is not None:
            consulta = consulta.filter(Evento.id == evento_id)
        elif usuario_id is not None:
            colaboradores = db.select(ColaboradorEvento.evento_id).where(
                ColaboradorEvento.usuario_id == usuario_id,
                ColaboradorEvento.status == "ativo",
            )
            consulta = consulta.filter(
                or_(Evento.owner_id == usuario_id, Evento.id.in_(colaboradores))
            )
        return consulta.all()
