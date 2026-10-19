from models import ItemCompartilhado, LogEvento
from repositories.item_repository import ItemRepository

from services.notificacoes_service import notificar_organizacao


def liberar_itens_colaborador(colaborador):
    for item in ItemRepository.do_colaborador(colaborador):
        item.responsavel_tipo = None
        item.responsavel_id = None
        item.responsavel_nome = ""
        LogEvento(
            evento_id=colaborador.evento_id,
            acao="item_liberado",
            detalhe=f"{colaborador.nome}: {item.nome} (fim da colaboração).",
        ).salvar(confirmar=False)


def liberar_itens_convidado(convidado):
    itens = ItemCompartilhado.listar(
        evento_id=convidado.evento_id,
        responsavel_tipo="convidado",
        responsavel_id=convidado.id,
    )
    for item in itens:
        item.responsavel_tipo = None
        item.responsavel_id = None
        item.responsavel_nome = ""
        LogEvento(
            evento_id=convidado.evento_id,
            acao="item_liberado",
            detalhe=f"{convidado.nome}: {item.nome} (saída da lista de participantes).",
        ).salvar(confirmar=False)
    if itens:
        notificar_organizacao(
            convidado.evento,
            "item-liberado",
            "Itens precisam de responsável",
            f"{convidado.nome} deixou de participar. Itens liberados: "
            + ", ".join((i.nome for i in itens)),
        )
