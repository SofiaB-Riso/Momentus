import os
from pathlib import Path
from uuid import uuid4

from application.erros import DadosInvalidos
from PIL import Image, UnidentifiedImageError
from werkzeug.utils import secure_filename


class ArquivosLocal:
    def __init__(self, pasta):
        self.pasta = Path(pasta)

    def salvar(self, arquivo, prefixo, extensoes):
        if not arquivo or not arquivo.filename:
            raise DadosInvalidos("Selecione um arquivo.")
        nome = secure_filename(arquivo.filename)
        extensao = nome.rsplit(".", 1)[-1].lower() if "." in nome else ""
        if not nome or extensao not in extensoes:
            raise DadosInvalidos("Formato de arquivo não suportado.")
        try:
            arquivo.stream.seek(0)
            if extensao == "pdf":
                if not arquivo.stream.read(5) == b"%PDF-":
                    raise DadosInvalidos("O arquivo não é um PDF válido.")
            else:
                imagem = Image.open(arquivo.stream)
                imagem.verify()
                esperados = {
                    "png": "PNG",
                    "jpg": "JPEG",
                    "jpeg": "JPEG",
                    "webp": "WEBP",
                    "gif": "GIF",
                }
                if imagem.format != esperados[extensao]:
                    raise DadosInvalidos(
                        "O conteúdo não corresponde ao formato da imagem."
                    )
        except (UnidentifiedImageError, OSError, Image.DecompressionBombError):
            raise DadosInvalidos("Imagem inválida.") from None
        finally:
            arquivo.stream.seek(0)
        self.pasta.mkdir(parents=True, exist_ok=True)
        nome_final = f"{prefixo}_{uuid4().hex}_{nome}"
        temporario = self.pasta / (nome_final + ".part")
        try:
            arquivo.save(temporario)
            os.replace(temporario, self.pasta / nome_final)
        finally:
            temporario.unlink(missing_ok=True)
        return nome_final

    def remover(self, nome):
        if nome and Path(nome).name == nome:
            (self.pasta / nome).unlink(missing_ok=True)
