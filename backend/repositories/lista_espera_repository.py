from models import Convidado, EntradaEspera, db


class ListaEsperaRepository:
    @staticmethod
    def confirmados(evento_id):
        db.session.flush()
        return Convidado.query.filter_by(
            evento_id=evento_id, status="confirmado"
        ).count()

    @staticmethod
    def fila(evento_id):
        return (
            EntradaEspera.query.filter_by(evento_id=evento_id, ativo=True)
            .join(Convidado)
            .filter(Convidado.status == "espera")
            .order_by(EntradaEspera.solicitado_em, EntradaEspera.id)
            .all()
        )

    @staticmethod
    def posicao(convidado):
        if convidado.status != "espera":
            return None
        fila = ListaEsperaRepository.fila(convidado.evento_id)
        return next(
            (i + 1 for i, e in enumerate(fila) if e.convidado_id == convidado.id), None
        )
