from repositories.consulta_evento_repository import ConsultaEventoRepository
from services.financeiro.resumo_financeiro_service import (
    CalcularResumoFinanceiroService,
)
from utils.mapas import links_mapa


def serializar_evento(evento, incluir_relacoes=True):
    """Enriquece a resposta sem fazer a Model depender da camada de serviços."""
    dados = evento.to_dict(incluir_relacoes=incluir_relacoes)
    metadados = ConsultaEventoRepository.metadados(evento.id)
    criacao = metadados["criado_em"]
    dados.update(
        revisao=metadados["revisao"],
        criado_em=criacao.isoformat() + "Z" if criacao else None,
        mapas=links_mapa(evento.endereco_evento, evento.cidade_evento),
        financeiro=CalcularResumoFinanceiroService().executar(evento),
        planejamento=evento.planejamento.to_dict()
        if evento.planejamento
        else {
            "duracao_minutos": 180,
            "limite_vagas": None,
            "cronograma_ativo": False,
            "cronograma_gerado_em": None,
        },
    )
    return dados


def aplicar_permissoes(dados, evento, usuario_id):
    dono = evento.owner_id == usuario_id
    colab = next(
        (
            c
            for c in evento.colaboradores_rel
            if c.usuario_id == usuario_id and c.status == "ativo"
        ),
        None,
    )
    pode_editar = dono or bool(colab and colab.pode_editar)
    dados.update(permissao="dono" if dono else "colaborador", pode_editar=pode_editar)
    if not dono:
        if not pode_editar:
            for convidado in dados.get("lista_convidados", []):
                convidado.pop("token_rsvp", None)
        for colaborador in dados.get("colaboradores", []):
            if colaborador["usuario_id"] != usuario_id:
                colaborador.pop("token", None)
    return dados
