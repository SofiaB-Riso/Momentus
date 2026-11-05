from datetime import datetime, timedelta, timezone

from models import AvisoConvidado, Evento, Notificacao, PreferenciasUsuario, db
from sqlalchemy import or_
from utils.tempo_local import fuso_local


class NotificacaoRepository:
    @staticmethod
    def listar(usuario_id):
        consulta = Notificacao.query.filter_by(usuario_id=usuario_id)
        prefs = PreferenciasUsuario.buscar_por_id(usuario_id)
        if prefs and not prefs.rsvp:
            consulta = consulta.filter(Notificacao.tipo != "rsvp")
        if prefs and not prefs.lembretes:
            consulta = consulta.filter(~Notificacao.tipo.startswith("lembrete-"))
        consulta = consulta.filter(
            or_(
                ~Notificacao.tipo.startswith("lembrete-"),
                Notificacao.evento_id.in_(
                    db.select(Evento.id).where(
                        Evento.status.in_(
                            ["agendado", "confirmado", "planejamento", "em_andamento"]
                        )
                    )
                ),
            )
        )
        return consulta.order_by(Notificacao.criado_em.desc()).limit(100).all()

    @staticmethod
    def marcar_lidas(usuario_id):
        Notificacao.query.filter_by(usuario_id=usuario_id, lida=False).update(
            {"lida": True}
        )

    @staticmethod
    def responder_convite(usuario_id, colaborador_id):
        Notificacao.query.filter_by(
            usuario_id=usuario_id,
            tipo="convite-colaborador",
            referencia_id=colaborador_id,
        ).update({"lida": True, "tipo": "convite-respondido"})

    @staticmethod
    def existente_hoje(hoje, **filtros):
        # criado_em é UTC sem tzinfo; o dia do lembrete é o dia local.
        inicio = (
            datetime.combine(hoje, datetime.min.time())
            .replace(tzinfo=fuso_local())
            .astimezone(timezone.utc)
            .replace(tzinfo=None)
        )
        fim = (
            datetime.combine(hoje + timedelta(days=1), datetime.min.time())
            .replace(tzinfo=fuso_local())
            .astimezone(timezone.utc)
            .replace(tzinfo=None)
        )
        return (
            Notificacao.query.filter_by(**filtros)
            .filter(
                Notificacao.criado_em >= inicio,
                Notificacao.criado_em < fim,
            )
            .first()
        )

    @staticmethod
    def avisos_convidado(convidado_id):
        return (
            AvisoConvidado.query.filter_by(convidado_id=convidado_id)
            .order_by(AvisoConvidado.criado_em.desc(), AvisoConvidado.id.desc())
            .limit(30)
            .all()
        )
