from models.evento_model import Evento
from datetime import date

class CriarEventoService:
    def executar(self, dados):
        campos_obrigatorios = ["nome_evento", "tipo_evento", "data_evento"]

        for campo in campos_obrigatorios:
            valor = dados.get(campo)
            if valor is None or (isinstance(valor, str) and not valor.strip()):
                raise ValueError(f"O campo '{campo}' é obrigatório.")

        evento = Evento(
            nome_evento=dados["nome_evento"],
            tipo_evento=dados["tipo_evento"],
            data_evento=date.fromisoformat(dados["data_evento"]),
            endereco_evento=dados.get("endereco_evento") or "",
            orcamento_evento=dados.get("orcamento_evento") or 0,
            dados_evento=dados.get("dados_evento"),
        )

        evento.salvar()
        return evento.to_dict()
