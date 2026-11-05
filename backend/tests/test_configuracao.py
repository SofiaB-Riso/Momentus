"""O SQLite relativo deve usar uma única instance, fora do diretório de execução."""

import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

os.environ["DATABASE_URL"] = "sqlite://"
import app as modulo_app
from models import Usuario, db


class ConfiguracaoBancoTest(unittest.TestCase):
    def test_sqlite_relativo_independe_do_diretorio_de_execucao(self):
        with tempfile.TemporaryDirectory() as pasta:
            raiz = Path(pasta)
            backend = raiz / "backend"
            backend.mkdir()
            with patch.object(modulo_app, "BASE_DIR", backend):
                app = modulo_app.create_app(
                    {
                        "TESTING": True,
                        "SQLALCHEMY_DATABASE_URI": "sqlite:///momentus.db",
                        "UPLOAD_FOLDER": str(raiz / "uploads"),
                    }
                )
                with app.app_context():
                    try:
                        self.assertEqual(Path(app.instance_path), backend / "instance")
                        self.assertEqual(
                            Path(db.engine.url.database),
                            backend / "instance/momentus.db",
                        )
                        self.assertEqual(Usuario.listar(), [])
                        self.assertFalse((raiz / "instance").exists())
                    finally:
                        db.session.remove()
                        db.engine.dispose()

    def test_sqlite_absoluto_continua_configuravel(self):
        with tempfile.TemporaryDirectory() as pasta:
            arquivo = Path(pasta) / "escolhido.db"
            app = modulo_app.create_app(
                {
                    "TESTING": True,
                    "SQLALCHEMY_DATABASE_URI": "sqlite:///" + str(arquivo),
                    "UPLOAD_FOLDER": pasta,
                }
            )
            with app.app_context():
                try:
                    self.assertEqual(Path(db.engine.url.database), arquivo)
                    self.assertEqual(Usuario.listar(), [])
                finally:
                    db.session.remove()
                    db.engine.dispose()
