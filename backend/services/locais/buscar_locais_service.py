from application.erros import DadosInvalidos
from utils.validacao import dinheiro, inteiro_positivo, normalizar

from services.caso_uso import CasoUso


class BuscarLocaisService(CasoUso):
    def executar(self, evento_id, params=None):
        _, evento = self.exigir_acesso_evento(evento_id)
        try:
            valor = params.get("orcamento")
            orcamento = (
                dinheiro(valor) if valor not in (None, "") else evento.orcamento_evento
            )
            capacidade = (
                inteiro_positivo(params["capacidade"])
                if params.get("capacidade")
                else max(evento.confirmados, evento.convidados_estimados, 1)
            )
        except ValueError as erro:
            raise DadosInvalidos(str(erro))
        cidade = normalizar(params.get("cidade", evento.cidade_evento))
        estilo = normalizar(params.get("estilo", evento.estilo_evento))
        resultados = []
        for local in evento.locais_rel:
            if cidade and cidade not in normalizar(local.cidade):
                continue
            if estilo and estilo not in normalizar(local.estilo):
                continue
            if local.capacidade < capacidade or (
                orcamento > 0 and local.preco > orcamento
            ):
                continue
            resultados.append(local.to_dict())
        resultados.sort(
            key=lambda registro: (
                registro["preco"],
                registro["capacidade"] - capacidade,
                registro["nome"],
            )
        )
        return {
            "locais": resultados,
            "total_salvos": len(evento.locais_rel),
            "filtros": {
                "orcamento": float(orcamento),
                "capacidade": capacidade,
                "cidade": cidade,
                "estilo": estilo,
            },
        }
