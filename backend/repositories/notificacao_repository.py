from datetime import datetime, timedelta, timezone

from models import AvisoConvidado, Notificacao


class NotificacaoRepository:
    @staticmethod
    def listar(usuario_id):
        return (
            Notificacao.query.filter_by(usuario_id=usuario_id)
            .order_by(Notificacao.criado_em.desc())
            .limit(100)
            .all()
        )

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
            .astimezone(timezone.utc)
            .replace(tzinfo=None)
        )
        fim = (
            datetime.combine(hoje + timedelta(days=1), datetime.min.time())
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
