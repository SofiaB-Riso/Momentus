from models import PrivacidadeUsuario

from services.caso_uso import CasoUso
from services.galeria.remover_arquivo_service import RemoverArquivoSemReferenciaService


class RemoverFotoPerfilService(CasoUso):
    def __init__(self, transacao, usuario_id, armazenamento):
        super().__init__(transacao, usuario_id)
        self.armazenamento = armazenamento

    def executar(self):
        registro = PrivacidadeUsuario.buscar_por_id(self.usuario_id)
        if registro and registro.foto_arquivo:
            nome = registro.foto_arquivo
            registro.foto_arquivo = None
            self.transacao.confirmar()
            RemoverArquivoSemReferenciaService(self.armazenamento).executar(
                nome, f"avatar{self.usuario_id}_"
            )
        return {"usuario": self.usuario_atual(exigir_autorizacao=False).to_dict()}
