from repositories.lista_espera_repository import ListaEsperaRepository

from services.caso_uso import CasoUso


class ConsultarListaEsperaService(CasoUso):
    def executar(self, evento_id):
        _, evento = self.exigir_acesso_evento(evento_id)
        limite = evento.planejamento.limite_vagas if evento.planejamento else None
        confirmados = ListaEsperaRepository.confirmados(evento.id)
        return {
            "limite_vagas": limite,
            "confirmados": confirmados,
            "vagas_livres": max(0, limite - confirmados)
            if limite is not None
            else None,
            "fila": [
                {
                    "id": e.convidado_id,
                    "nome": e.convidado.nome,
                    "posicao": i + 1,
                    "solicitado_em": e.solicitado_em.isoformat() + "Z",
                }
                for i, e in enumerate(ListaEsperaRepository.fila(evento.id))
            ],
        }
