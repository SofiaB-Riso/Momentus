from models import DespesaEvento, FotoEvento


def arquivos_do_evento(evento_id):
    return [foto.arquivo for foto in FotoEvento.listar(evento_id=evento_id)] + [
        despesa.comprovante
        for despesa in DespesaEvento.listar(evento_id=evento_id)
        if despesa.comprovante
    ]
