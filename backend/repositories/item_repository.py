from models import Convidado, ItemCompartilhado
from sqlalchemy import and_, or_


class ItemRepository:
    @staticmethod
    def liberar_convidado(item_id, convidado_id):
        return ItemCompartilhado.query.filter_by(
            id=item_id, responsavel_tipo="convidado", responsavel_id=convidado_id
        ).update(
            {"responsavel_tipo": None, "responsavel_id": None, "responsavel_nome": ""}
        )

    @staticmethod
    def reservar_convidado(item_id, evento_id, convidado):
        return (
            ItemCompartilhado.query.filter_by(id=item_id, evento_id=evento_id)
            .filter(
                or_(
                    ItemCompartilhado.responsavel_nome.is_(None),
                    ItemCompartilhado.responsavel_nome == "",
                )
            )
            .update(
                {
                    "responsavel_tipo": "convidado",
                    "responsavel_id": convidado.id,
                    "responsavel_nome": convidado.nome,
                }
            )
        )

    @staticmethod
    def atualizar_reserva(item_id, evento_id, valores, pessoa=None, tipo=None):
        consulta = ItemCompartilhado.query.filter_by(id=item_id, evento_id=evento_id)
        if pessoa is not None:
            consulta = consulta.filter(
                or_(
                    ItemCompartilhado.responsavel_nome.is_(None),
                    ItemCompartilhado.responsavel_nome == "",
                    and_(
                        ItemCompartilhado.responsavel_tipo == tipo,
                        ItemCompartilhado.responsavel_id == pessoa.id,
                    ),
                )
            )
        return consulta.update(valores)

    @staticmethod
    def convidado_participante(convidado_id, evento_id):
        return (
            Convidado.query.filter_by(id=convidado_id, evento_id=evento_id)
            .filter(Convidado.status != "recusado")
            .first()
        )

    @staticmethod
    def atualizar_nome_convidado(convidado):
        ItemCompartilhado.query.filter_by(
            evento_id=convidado.evento_id,
            responsavel_tipo="convidado",
            responsavel_id=convidado.id,
        ).update({"responsavel_nome": convidado.nome})

    @staticmethod
    def do_colaborador(colaborador):
        criterios = [
            and_(
                ItemCompartilhado.responsavel_tipo == "colaborador",
                ItemCompartilhado.responsavel_id == colaborador.id,
            )
        ]
        if colaborador.usuario_id:
            criterios.append(
                and_(
                    ItemCompartilhado.responsavel_tipo == "usuario",
                    ItemCompartilhado.responsavel_id == colaborador.usuario_id,
                )
            )
        return ItemCompartilhado.query.filter(
            ItemCompartilhado.evento_id == colaborador.evento_id, or_(*criterios)
        ).all()
