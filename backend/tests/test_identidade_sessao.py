"""A sessão não deve trocar de pessoa quando um banco reutiliza o mesmo ID."""

import os
import tempfile
import unittest
from pathlib import Path

os.environ["DATABASE_URL"] = "sqlite://"
from app import create_app
from models import Usuario, db


class IdentidadeSessaoTest(unittest.TestCase):
    def setUp(self):
        self.pasta = tempfile.TemporaryDirectory(prefix="momentus-identidade-")
        self.apps = []
        self.app = self.novo_app("primeiro.db")
        self.cliente = self.app.test_client()
        resposta = self.cliente.post(
            "/auth/cadastro",
            json={
                "nome": "Cícero teste",
                "email": "cicero@teste.example",
                "senha": "senha-teste",
            },
        )
        self.assertEqual(resposta.status_code, 201)
        self.ident = resposta.json["usuario"]["id"]

    def novo_app(self, nome):
        app = create_app(
            {
                "TESTING": True,
                "SECRET_KEY": "mesma-chave-de-teste",
                "SQLALCHEMY_DATABASE_URI": "sqlite:///"
                + str(Path(self.pasta.name) / nome),
                "UPLOAD_FOLDER": self.pasta.name,
                "GOOGLE_MAPS_API_KEY": "simulada",
            }
        )
        self.apps.append(app)
        return app

    def tearDown(self):
        for app in self.apps:
            with app.app_context():
                db.session.remove()
                db.engine.dispose()
        self.pasta.cleanup()

    def test_sessao_antiga_apenas_com_id_e_rejeitada(self):
        cliente = self.app.test_client()
        with cliente.session_transaction() as sessao:
            sessao["usuario_id"] = self.ident
        resposta = cliente.get("/auth/me")
        self.assertEqual(resposta.status_code, 401)
        with cliente.session_transaction() as sessao:
            self.assertNotIn("usuario_id", sessao)

    def test_trocar_banco_com_mesmo_id_nao_abre_outra_conta(self):
        segundo = self.novo_app("segundo.db")
        cliente = segundo.test_client()
        outra = cliente.post(
            "/auth/cadastro",
            json={
                "nome": "Luiza teste",
                "email": "luiza@teste.example",
                "senha": "outra-senha",
            },
        )
        self.assertEqual(outra.json["usuario"]["id"], self.ident)
        cliente.set_cookie("session", self.cliente.get_cookie("session").value)
        self.assertEqual(cliente.get("/auth/me").status_code, 401)
        # O novo login explícito continua aceitando a conta escolhida.
        login = cliente.post(
            "/auth/login", json={"email": "luiza@teste.example", "senha": "outra-senha"}
        )
        self.assertEqual(login.status_code, 200)
        self.assertEqual(cliente.get("/auth/me").json["usuario"]["nome"], "Luiza teste")

    def test_trocar_apenas_o_id_nao_aceita_identidade_de_outra_pessoa(self):
        outra = self.app.test_client()
        resposta = outra.post(
            "/auth/cadastro",
            json={
                "nome": "Outra pessoa",
                "email": "outra@teste.example",
                "senha": "outra-senha",
            },
        )
        with self.cliente.session_transaction() as sessao:
            sessao["usuario_id"] = resposta.json["usuario"]["id"]
        self.assertEqual(self.cliente.get("/auth/me").status_code, 401)

    def test_reiniciar_mesmo_banco_preserva_a_pessoa_correta(self):
        with self.cliente.session_transaction() as sessao:
            self.assertEqual(sessao["usuario_id"], self.ident)
            self.assertEqual(len(sessao["usuario_identidade"]), 64)
            self.assertNotIn("senha_hash", sessao)
        reiniciado = self.novo_app("primeiro.db").test_client()
        reiniciado.set_cookie("session", self.cliente.get_cookie("session").value)
        resposta = reiniciado.get("/auth/me")
        self.assertEqual(resposta.status_code, 200)
        self.assertEqual(resposta.json["usuario"]["email"], "cicero@teste.example")

    def test_editar_perfil_nao_troca_pessoa_nem_derruba_login(self):
        resposta = self.cliente.put(
            "/auth/perfil",
            json={"nome": "Cícero atualizado", "email": "cicero.novo@teste.example"},
        )
        self.assertEqual(resposta.status_code, 200)
        perfil = self.cliente.get("/auth/me")
        self.assertEqual(perfil.status_code, 200)
        self.assertEqual(perfil.json["usuario"]["id"], self.ident)
        self.assertEqual(perfil.json["usuario"]["email"], "cicero.novo@teste.example")

    def test_substituir_credencial_do_cadastro_invalida_sessao(self):
        with self.app.app_context():
            usuario = Usuario.buscar_por_id(self.ident)
            usuario.definir_senha("nova-senha")
            db.session.commit()
        self.assertEqual(self.cliente.get("/auth/me").status_code, 401)
