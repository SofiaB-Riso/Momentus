from pathlib import Path

from repositories.arquivo_repository import ArquivoRepository


class RemoverArquivoSemReferenciaService:
    """Só remove arquivos do escopo esperado e sem vínculos no banco."""

    def __init__(self, armazenamento):
        self.armazenamento = armazenamento

    def executar(self, nome, prefixo):
        if (
            nome
            and Path(nome).name == nome
            and nome.startswith(prefixo)
            and not ArquivoRepository.possui_referencias(nome)
        ):
            self.armazenamento.remover(nome)
