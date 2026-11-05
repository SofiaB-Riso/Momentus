from models import DespesaEvento, FotoEvento


class ListarArquivosEventoService:
    def executar(self, evento_id):
        return [
            (foto.arquivo, f"evento{evento_id}_")
            for foto in FotoEvento.listar(evento_id=evento_id)
        ] + [
            (despesa.comprovante, f"comprovante_evento{evento_id}_{despesa.id}_")
            for despesa in DespesaEvento.listar(evento_id=evento_id)
            if despesa.comprovante
        ]
