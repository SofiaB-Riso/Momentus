from models.evento_model import Evento
from datetime import date

class AtualizarEventoService:
    def executar(self, evento_id, dados):
        evento = Evento.buscar_por_id(evento_id)

        if evento is None:
            return None

        # Antes esta linha quebrava (erro 500) sempre que "data_evento"
        # não vinha no payload, porque acessava dados["data_evento"]
        # direto. Agora só converte quando o campo é realmente enviado.
        data_evento = date.fromisoformat(dados["data_evento"]) if dados.get("data_evento") else None

        evento.atualizar(
            nome_evento=dados.get("nome_evento"),
            tipo_evento=dados.get("tipo_evento"),
            data_evento=data_evento,
            endereco_evento=dados.get("endereco_evento"),
            orcamento_evento=dados.get("orcamento_evento"),
            dados_evento=dados.get("dados_evento"),
        )

        return evento.to_dict()
