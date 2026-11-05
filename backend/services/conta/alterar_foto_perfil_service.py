from models import PrivacidadeUsuario

from services.caso_uso import CasoUso
from services.galeria.remover_arquivo_service import RemoverArquivoSemReferenciaService


class AlterarFotoPerfilService(CasoUso):
    def __init__(self, transacao, usuario_id, armazenamento):
        super().__init__(transacao, usuario_id)
        self.armazenamento = armazenamento

    def executar(self, arquivo):
        usuario = self.usuario_atual(exigir_autorizacao=False)
        registro = PrivacidadeUsuario.buscar_por_id(usuario.id)
        if registro is None:
            registro = PrivacidadeUsuario(usuario_id=usuario.id).salvar(confirmar=False)
        anterior = registro.foto_arquivo
        nome = self.armazenamento.salvar_avatar(arquivo, usuario.id)
        try:
            registro.foto_arquivo = nome
            self.transacao.confirmar()
        except Exception:
            self.transacao.reverter()
            self.armazenamento.remover(nome)
            raise
        RemoverArquivoSemReferenciaService(self.armazenamento).executar(
            anterior, f"avatar{usuario.id}_"
        )
        return {"usuario": usuario.to_dict()}
