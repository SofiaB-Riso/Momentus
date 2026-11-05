from services.caso_uso import CasoUso


class ListarConvidadosService(CasoUso):
    def executar(self, evento_id):
        usuario, evento = self.exigir_acesso_evento(evento_id)
        return [
            c.to_dict(
                incluir_token=bool(
                    evento.owner_id == usuario.id
                    or any(
                        (
                            c.usuario_id == usuario.id
                            and c.status == "ativo"
                            and c.pode_editar
                            for c in evento.colaboradores_rel
                        )
                    )
                )
            )
            for c in evento.convidados_rel
        ]
