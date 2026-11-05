import json
from decimal import Decimal

from application.erros import DadosInvalidos
from repositories.proposta_repository import PropostaRepository
from utils.validacao import dinheiro

from services.caso_uso import CasoUso
from services.propostas.validacao import CATEGORIAS, SERVICOS


class CompararPropostasService(CasoUso):
    def executar(self, evento_id, params=None):
        _, evento = self.exigir_acesso_evento(evento_id)
        params = params or {}
        categoria = params.get("categoria", "buffet")
        if categoria not in CATEGORIAS:
            raise DadosInvalidos("Categoria inválida.")
        necessarios = set(filter(None, (params.get("necessarios") or "").split(",")))
        if not necessarios <= SERVICOS:
            raise DadosInvalidos("Serviços necessários inválidos.")
        teto = (
            dinheiro(params["teto"])
            if params.get("teto") not in (None, "")
            else (
                max(
                    Decimal(0),
                    Decimal(evento.orcamento_evento) - evento.total_despesas_decimal,
                )
                if evento.orcamento_evento
                else None
            )
        )
        propostas = PropostaRepository.por_categoria(evento.id, categoria)
        linhas = []
        for p in propostas:
            faltantes = sorted(necessarios - set(json.loads(p.servicos_json)))
            dentro = teto is None or p.total <= teto
            linhas.append(
                (
                    p,
                    dict(
                        p.to_dict(),
                        faltantes=faltantes,
                        atende_requisitos=not faltantes,
                        dentro_orcamento=dentro,
                        adequada=not faltantes and dentro,
                    ),
                )
            )
        linhas.sort(
            key=lambda item: (
                not item[1]["adequada"],
                len(item[1]["faltantes"]),
                item[0].total,
                item[0].id,
            )
        )
        melhor = next((p for p in linhas if p[1]["adequada"]), None)
        resultado = [
            dict(p[1], destaque=bool(melhor and p[0].id == melhor[0].id))
            for p in linhas
        ]
        return {
            "categoria": categoria,
            "teto": float(teto) if teto is not None else None,
            "propostas": resultado,
            "menor_valor": float(min(p.total for p in propostas))
            if propostas
            else None,
            "economia_possivel": float(
                max(p.total for p in propostas) - min(p.total for p in propostas)
            )
            if propostas
            else 0,
            "criterio": "Opções dentro do teto e com todos os serviços necessários primeiro; depois, menor total com desconto e taxas. Qualidade e disponibilidade devem ser confirmadas.",
        }
