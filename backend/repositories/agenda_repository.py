from repositories.consulta_evento_repository import ConsultaEventoRepository


class AgendaRepository:
    @staticmethod
    def eventos_do_usuario(usuario_id, exceto_id=None):
        return [
            e
            for e in ConsultaEventoRepository.acessiveis(usuario_id)
            if e.id != exceto_id
            and e.status not in {"rascunho", "cancelado", "concluido"}
        ]
