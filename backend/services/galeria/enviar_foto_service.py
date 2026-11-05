from application.contratos import ArmazenamentoArquivos, Criado
from models import FotoEvento

from services.caso_uso import CasoUso


class EnviarFotoService(CasoUso):
    def __init__(self, transacao, usuario_id, armazenamento: ArmazenamentoArquivos):
        super().__init__(transacao, usuario_id)
        self.armazenamento = armazenamento

    def executar(self, evento_id, arquivo, legenda=""):
        usuario, evento = self.exigir_acesso_evento(evento_id, exigir_edicao=True)
        if not isinstance(legenda, str) or len(legenda.strip()) > 255:
            raise ValueError("A legenda deve ter até 255 caracteres.")
        nome = self.armazenamento.salvar(
            arquivo, f"evento{evento.id}", {"png", "jpg", "jpeg", "webp", "gif"}
        )
        try:
            foto = FotoEvento(
                evento_id=evento.id,
                usuario_id=usuario.id,
                arquivo=nome,
                legenda=legenda.strip(),
            ).salvar(confirmar=False)
            self.log(evento.id, "foto_adicionada", foto.legenda or "Foto do evento")
            self.transacao.confirmar()
            return Criado(foto.to_dict())
        except Exception:
            self.transacao.reverter()
            self.armazenamento.remover(nome)
            raise
