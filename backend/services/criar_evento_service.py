from models.evento_model import Evento
from datetime import date

class CriarEventoService:
    def executar(self, dados):
        campos_obrigatorios = ["nome_evento", "tipo_evento", "data_evento", "endereco_evento", "orcamento_evento"]

        for campo in campos_obrigatorios:
            if not dados.get(campo):
                raise ValueError(f"O campo '{campo}' é obrigatório.")

        evento = Evento(
            nome_evento=dados["nome_evento"],
            tipo_evento=dados["tipo_evento"],
            data_evento = date.fromisoformat(dados["data_evento"]),
            endereco_evento=dados["endereco_evento"],
            orcamento_evento=dados["orcamento_evento"],
        )

        evento.salvar()
        return evento.to_dict()
