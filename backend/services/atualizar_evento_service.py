from datetime import date

from models import Evento, db


class AtualizarEventoService:
    def executar(self, evento_id, dados):
        evento = Evento.buscar_por_id(evento_id)
        if evento is None:
            return None

        mapeamento_texto = {
            "nome_evento": "nome_evento",
            "tipo_evento": "tipo_evento",
            "hora_evento": "hora_evento",
            "endereco_evento": "endereco_evento",
            "cidade_evento": "cidade_evento",
            "estilo_evento": "estilo_evento",
            "observacoes": "observacoes",
            "status": "status",
            "privacidade_convidados": "privacidade_convidados",
            "dados_evento": "dados_evento",
        }
        for entrada, atributo in mapeamento_texto.items():
            if entrada in dados:
                setattr(evento, atributo, dados.get(entrada) if entrada == "dados_evento" else (dados.get(entrada) or "").strip())

        if dados.get("data_evento"):
            try:
                evento.data_evento = date.fromisoformat(dados["data_evento"])
            except ValueError:
                raise ValueError("'data_evento' deve estar no formato AAAA-MM-DD.")
        if "orcamento_evento" in dados:
            evento.orcamento_evento = max(0, float(dados.get("orcamento_evento") or 0))
        if "convidados_estimados" in dados:
            evento.convidados_estimados = max(0, int(dados.get("convidados_estimados") or 0))
        if "progresso" in dados:
            evento.progresso = max(0, min(100, int(dados.get("progresso") or 0)))
        if "rateio" in dados and isinstance(dados["rateio"], dict):
            rateio = dados["rateio"]
            if "ativo" in rateio:
                evento.rateio_ativo = bool(rateio["ativo"])
            if "modo" in rateio:
                evento.rateio_modo = rateio.get("modo") or "auto"
            if "valorFixo" in rateio:
                evento.rateio_valor_fixo = max(0, float(rateio.get("valorFixo") or 0))

        db.session.commit()
        return evento.to_dict()
