import os
from pathlib import Path
from uuid import uuid4

from application.erros import DadosInvalidos
from PIL import Image, ImageOps, UnidentifiedImageError
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

    def salvar_avatar(self, arquivo, usuario_id):
        """Reencoda a imagem sem EXIF ou nome original, com tamanho limitado."""
        if not arquivo or not arquivo.filename:
            raise DadosInvalidos("Selecione uma imagem PNG, JPEG ou WebP.")
        self.pasta.mkdir(parents=True, exist_ok=True)
        nome = f"avatar{usuario_id}_{uuid4().hex}.webp"
        temporario = self.pasta / (nome + ".part")
        try:
            with Image.open(arquivo.stream) as imagem:
                if (
                    imagem.format not in {"PNG", "JPEG", "WEBP"}
                    or imagem.width * imagem.height > 20_000_000
                ):
                    raise DadosInvalidos("Use PNG, JPEG ou WebP com até 20 megapixels.")
                imagem.load()
                convertida = ImageOps.exif_transpose(imagem).convert("RGB")
                convertida.thumbnail((512, 512))
                convertida.save(temporario, "WEBP", quality=85, exif=b"")
            os.replace(temporario, self.pasta / nome)
        except (UnidentifiedImageError, OSError, Image.DecompressionBombError):
            raise DadosInvalidos("A imagem selecionada é inválida.") from None
        finally:
            temporario.unlink(missing_ok=True)
        return nome
