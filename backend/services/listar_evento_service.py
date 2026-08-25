from sqlalchemy import or_

from models import ColaboradorEvento, Evento


class ListarEventosService:
    def executar(self, usuario_id):
        eventos = (
            Evento.query.outerjoin(
                ColaboradorEvento,
                (ColaboradorEvento.evento_id == Evento.id)
                & (ColaboradorEvento.usuario_id == usuario_id)
                & (ColaboradorEvento.status == "ativo"),
            )
            .filter(or_(Evento.owner_id == usuario_id, ColaboradorEvento.id.isnot(None)))
            .order_by(Evento.data_evento.asc(), Evento.id.asc())
            .distinct()
            .all()
        )
        resposta = []
        for evento in eventos:
            dados = evento.to_dict()
            if evento.owner_id == usuario_id:
                dados["permissao"] = "dono"
                dados["pode_editar"] = True
            else:
                colab = next((c for c in evento.colaboradores_rel if c.usuario_id == usuario_id and c.status == "ativo"), None)
                dados["permissao"] = "colaborador"
                dados["pode_editar"] = bool(colab and colab.pode_editar)
            resposta.append(dados)
        return resposta
