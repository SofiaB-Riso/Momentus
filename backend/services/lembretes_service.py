from datetime import date, datetime, timedelta

from models import Notificacao
from repositories.consulta_evento_repository import ConsultaEventoRepository
from repositories.notificacao_repository import NotificacaoRepository

from services.notificacoes_service import adicionar_aviso


def gerar_lembretes(usuario_id=None, evento_id=None, transacao=None):
    """Idempotente por dia; usado automaticamente nas centrais e pelo comando CLI."""
    if transacao is None:
        raise ValueError("Informe a transação para gerar lembretes.")
    hoje = date.today()
    for evento in ConsultaEventoRepository.para_lembretes(hoje, usuario_id, evento_id):
        ConsultaEventoRepository.bloquear(evento.id, renovar=False)
        destinatarios = {evento.owner_id} | {
            c.usuario_id
            for c in evento.colaboradores_rel
            if c.status == "ativo" and c.usuario_id
        }
        pendentes = sum((c.status == "pendente" for c in evento.convidados_rel))
        livres = sum((not i.responsavel_nome for i in evento.itens_compartilhados_rel))
        avisos = [
            (
                "lembrete-evento",
                "Evento se aproximando",
                f"{evento.nome_evento}: confira os preparativos.",
            )
        ]
        proximo = evento.data_evento <= hoje + timedelta(days=2)
        if not proximo:
            avisos = []
        if pendentes and proximo:
            avisos.append(
                (
                    "lembrete-presenca",
                    "Presenças pendentes",
                    f"{evento.nome_evento}: {pendentes} pessoa(s) ainda não responderam.",
                )
            )
        if livres and proximo:
            avisos.append(
                (
                    "lembrete-itens",
                    "Itens sem responsável",
                    f"{evento.nome_evento}: {livres} item(ns) ainda precisam de alguém para levar.",
                )
            )
        for usuario in destinatarios:
            for tipo, titulo, mensagem in avisos:
                existente = NotificacaoRepository.existente_hoje(
                    hoje, usuario_id=usuario, evento_id=evento.id, tipo=tipo
                )
                if not existente:
                    Notificacao(
                        usuario_id=usuario,
                        evento_id=evento.id,
                        tipo=tipo,
                        titulo=titulo,
                        mensagem=mensagem,
                    ).salvar(confirmar=False)
            for tarefa in evento.tarefas_rel:
                if (
                    tarefa.feita
                    or not tarefa.prazo
                    or tarefa.prazo > datetime.now() + timedelta(days=2)
                ):
                    continue
                existe = NotificacaoRepository.existente_hoje(
                    hoje,
                    usuario_id=usuario,
                    tipo="lembrete-tarefa",
                    referencia_id=tarefa.id,
                )
                if not existe:
                    Notificacao(
                        usuario_id=usuario,
                        evento_id=evento.id,
                        tipo="lembrete-tarefa",
                        referencia_id=tarefa.id,
                        titulo="Tarefa pendente",
                        mensagem=f"{evento.nome_evento}: {tarefa.titulo}.",
                    ).salvar(confirmar=False)
        for convidado in evento.convidados_rel if proximo else []:
            if convidado.status == "pendente":
                adicionar_aviso(
                    convidado,
                    "Você vai?",
                    "Confirme sua presença para ajudar nos preparativos.",
                    f"presenca:{hoje}",
                )
            if livres and convidado.status != "recusado":
                adicionar_aviso(
                    convidado,
                    "Vamos dividir os preparativos?",
                    f"Há {livres} item(ns) disponíveis na lista compartilhada.",
                    f"itens:{hoje}",
                )
    transacao.confirmar()
