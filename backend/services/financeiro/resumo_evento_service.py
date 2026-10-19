import math

from models import Fornecedor
from utils.mapas import links_mapa
from utils.validacao import normalizar

from services.caso_uso import CasoUso
from services.financeiro.resumo_financeiro_service import resumo_financeiro


class ResumoEventoService(CasoUso):
    def executar(self, evento_id):
        _, evento = self.exigir_acesso_evento(evento_id)
        confirmados = evento.confirmados
        base = max(confirmados, evento.convidados_estimados or 0)
        suprimentos = {
            "pessoas_consideradas": base,
            "comida_kg": round(base * 0.45, 1),
            "bebidas_litros": round(base * 0.8, 1),
            "gelo_kg": round(base * 0.2, 1),
            "doces_unidades": math.ceil(base * 5),
        }
        restricoes = [
            f"{c.nome}: {c.restricoes_alimentares}"
            for c in evento.convidados_rel
            if c.restricoes_alimentares and c.status != "recusado"
        ]
        perfil_custos = {
            "casamento": {
                "alimentacao_por_pessoa": 140,
                "bebida_por_pessoa": 45,
                "decoracao": 8000,
                "local": 6000,
            },
            "aniversario": {
                "alimentacao_por_pessoa": 80,
                "bebida_por_pessoa": 25,
                "decoracao": 2500,
                "local": 2500,
            },
            "corporativo": {
                "alimentacao_por_pessoa": 110,
                "bebida_por_pessoa": 30,
                "decoracao": 3000,
                "local": 4500,
            },
        }
        custo = perfil_custos.get(
            (evento.tipo_evento or "").lower(),
            {
                "alimentacao_por_pessoa": 90,
                "bebida_por_pessoa": 30,
                "decoracao": 3000,
                "local": 3000,
            },
        )
        orcamento_base = {
            "alimentacao": round(base * custo["alimentacao_por_pessoa"], 2),
            "bebidas": round(base * custo["bebida_por_pessoa"], 2),
            "decoracao": float(custo["decoracao"]),
            "local": float(custo["local"]),
        }
        orcamento_base["total_estimado"] = round(sum(orcamento_base.values()), 2)
        fornecedores = [
            f
            for f in Fornecedor.listar(ativo=True)
            if not evento.cidade_evento
            or normalizar(evento.cidade_evento) in normalizar(f.cidade)
        ]
        fornecedores.sort(
            key=lambda f: (
                normalizar(evento.tipo_evento)
                in normalizar((f.descricao or "") + " " + f.tipo_servico),
                float(f.avaliacao or 0),
            ),
            reverse=True,
        )
        fornecedores = fornecedores[:6]
        locais = [
            registro
            for registro in evento.locais_rel
            if registro.capacidade >= base
            and (
                not evento.orcamento_evento or registro.preco <= evento.orcamento_evento
            )
            and (
                not evento.cidade_evento
                or normalizar(evento.cidade_evento) in normalizar(registro.cidade)
            )
            and (
                not evento.estilo_evento
                or normalizar(evento.estilo_evento) in normalizar(registro.estilo)
            )
        ]
        return {
            "financeiro": resumo_financeiro(evento),
            "convidados": {
                "estimados": evento.convidados_estimados,
                "confirmados": confirmados,
                "pendentes": sum(
                    (1 for c in evento.convidados_rel if c.status == "pendente")
                ),
                "recusados": sum(
                    (1 for c in evento.convidados_rel if c.status == "recusado")
                ),
                "restricoes_alimentares": restricoes,
            },
            "suprimentos": suprimentos,
            "orcamento_base": orcamento_base,
            "mapa_url": links_mapa(evento.endereco_evento, evento.cidade_evento)[
                "google"
            ],
            "mapas": links_mapa(evento.endereco_evento, evento.cidade_evento),
            "fornecedores_recomendados": [
                f.to_dict(incluir_produtos=False) for f in fornecedores
            ],
            "locais_recomendados": [f.to_dict() for f in locais],
        }
