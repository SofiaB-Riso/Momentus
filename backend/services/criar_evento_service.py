from datetime import date

from models import Evento, TarefaEvento, db


TAREFAS_PADRAO = [
    ("checklistLocal", "Escolha o local"),
    ("checklistCardapio", "Defina o cardápio"),
    ("checklistConvites", "Envie os convites"),
    ("checklistFornecedores", "Confirme os fornecedores"),
]


class CriarEventoService:
    def executar(self, dados, owner_id):
        for campo in ("nome_evento", "tipo_evento", "data_evento"):
            valor = dados.get(campo)
            if valor is None or (isinstance(valor, str) and not valor.strip()):
                raise ValueError(f"O campo '{campo}' é obrigatório.")

        try:
            data_evento = date.fromisoformat(dados["data_evento"])
        except (TypeError, ValueError):
            raise ValueError("'data_evento' deve estar no formato AAAA-MM-DD.")

        evento = Evento(
            owner_id=owner_id,
            nome_evento=str(dados["nome_evento"]).strip(),
            tipo_evento=str(dados["tipo_evento"]).strip(),
            data_evento=data_evento,
            hora_evento=(dados.get("hora_evento") or "").strip(),
            endereco_evento=(dados.get("endereco_evento") or "").strip(),
            cidade_evento=(dados.get("cidade_evento") or "").strip(),
            orcamento_evento=max(0, float(dados.get("orcamento_evento") or 0)),
            convidados_estimados=max(0, int(dados.get("convidados_estimados") or 0)),
            estilo_evento=(dados.get("estilo_evento") or "").strip(),
            observacoes=(dados.get("observacoes") or "").strip(),
            status=(dados.get("status") or "agendado").strip(),
            progresso=max(0, min(100, int(dados.get("progresso") or 0))),
            privacidade_convidados=(dados.get("privacidade_convidados") or "organizador").strip(),
            dados_evento=dados.get("dados_evento"),
        )
        db.session.add(evento)
        db.session.flush()

        for ordem, (chave, titulo) in enumerate(TAREFAS_PADRAO):
            db.session.add(TarefaEvento(evento_id=evento.id, chave=chave, titulo=titulo, ordem=ordem))

        db.session.commit()
        return evento.to_dict()
