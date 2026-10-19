from repositories.notificacao_repository import NotificacaoRepository
from utils.mapas import links_mapa


def dados_rsvp(convidado):
    evento = convidado.evento
    itens = []
    for item in evento.itens_compartilhados_rel:
        dados = item.to_dict()
        meu = (
            item.responsavel_tipo == "convidado" and item.responsavel_id == convidado.id
        )
        if not meu:
            dados["responsavelId"] = None
            dados["responsavelNome"] = "Já reservado" if item.responsavel_nome else ""
        itens.append(dados)
    avisos = NotificacaoRepository.avisos_convidado(convidado.id)
    livres = any((not i.responsavel_nome for i in evento.itens_compartilhados_rel))
    avisos = [
        a
        for a in avisos
        if (not a.chave.startswith("presenca:") or convidado.status == "pendente")
        and (
            not a.chave.startswith("itens:")
            or (livres and convidado.status != "recusado")
        )
    ]
    avisos_publicos = []
    for aviso in avisos:
        dados = aviso.to_dict()
        if aviso.chave.startswith("itens:"):
            dados["mensagem"] = (
                "Ainda há itens disponíveis na lista compartilhada. Você pode escolher o que levar."
            )
        avisos_publicos.append(dados)
    return {
        "convidado": convidado.to_dict(incluir_token=False),
        "avisos": avisos_publicos,
        "evento": {
            "nome": evento.nome_evento,
            "tipo": evento.tipo_evento,
            "data": evento.data_evento.isoformat(),
            "hora": evento.hora_evento or "",
            "local": evento.endereco_evento or "",
            "cidade": evento.cidade_evento or "",
            "mapas": links_mapa(evento.endereco_evento, evento.cidade_evento),
            "organizador": evento.owner.nome if evento.owner else "Momentus",
            "confirmados_publicos": [
                c.nome for c in evento.convidados_rel if c.status == "confirmado"
            ]
            if evento.privacidade_convidados == "todos"
            else [],
            "itens_compartilhados": itens,
        },
    }
