from services.caso_uso import CasoUso


class ListarDespesasService(CasoUso):
    def executar(self, evento_id):
        _, evento = self.exigir_acesso_evento(evento_id)
        return [d.to_dict() for d in evento.despesas_rel]
