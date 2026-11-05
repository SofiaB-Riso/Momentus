import hashlib
import json
import sqlite3
import tempfile
import unittest
from pathlib import Path
from zipfile import ZipFile

from scripts.backup import criar_backup, restaurar_backup


class BackupTest(unittest.TestCase):
    def test_restauracao_recusa_caminho_externo_e_manifesto_alterado(self):
        with tempfile.TemporaryDirectory() as pasta:
            raiz = Path(pasta)
            banco = raiz / "origem.db"
            with sqlite3.connect(banco) as db:
                db.execute("CREATE TABLE exemplo (id INTEGER PRIMARY KEY)")
            conteudo = banco.read_bytes()
            for nome in ["uploads/../../fora.txt", "uploads/arquivo.txt"]:
                arquivo = raiz / "corrompido.zip"
                with ZipFile(arquivo, "w") as zipado:
                    zipado.writestr(
                        "manifesto.json",
                        json.dumps(
                            {
                                "versao": 1,
                                "arquivos": {
                                    "banco.db": hashlib.sha256(conteudo).hexdigest(),
                                    nome: hashlib.sha256(b"conteudo").hexdigest()
                                    if ".." in nome
                                    else "hash-incorreto",
                                },
                            }
                        ),
                    )
                    zipado.writestr("banco.db", conteudo)
                    zipado.writestr(nome, b"conteudo")
                with self.assertRaises(ValueError):
                    restaurar_backup(arquivo, raiz / "destino")
                self.assertFalse((raiz / "destino").exists())
                self.assertFalse((raiz / "fora.txt").exists())

    def test_backup_restaura_banco_upload_e_segredo_em_pasta_nova(self):
        with tempfile.TemporaryDirectory() as pasta:
            raiz = Path(pasta)
            banco = raiz / "origem.db"
            uploads = raiz / "uploads"
            uploads.mkdir()
            with sqlite3.connect(banco) as db:
                db.execute("CREATE TABLE exemplo (id INTEGER PRIMARY KEY, valor TEXT)")
                db.execute("INSERT INTO exemplo VALUES (1, ?)", ("registro de teste",))
            (uploads / "foto.png").write_bytes(b"imagem de teste")
            (raiz / ".session-secret").write_text("segredo-de-teste")
            copia = criar_backup(banco, uploads, raiz / "backup.zip")
            destino = restaurar_backup(copia, raiz / "restaurado")
            with sqlite3.connect(destino / "backend/instance/momentus.db") as db:
                self.assertEqual(
                    db.execute("SELECT valor FROM exemplo").fetchone()[0],
                    "registro de teste",
                )
            self.assertEqual(
                (destino / "backend/uploads/foto.png").read_bytes(), b"imagem de teste"
            )
            self.assertEqual(
                (destino / "backend/instance/.session-secret").read_text(),
                "segredo-de-teste",
            )
            with self.assertRaises(ValueError):
                restaurar_backup(copia, destino)
            with self.assertRaises(FileExistsError):
                criar_backup(banco, uploads, copia)
