"""Fluxos de privacidade e recuperação, com SMTP e banco temporários."""

import io
import os
import tempfile
import unittest
from datetime import timedelta
from pathlib import Path
from unittest.mock import patch
from urllib.parse import parse_qs, urlsplit

os.environ["DATABASE_URL"] = "sqlite://"
from app import create_app
from application.erros import IntegracaoIndisponivel
from models import PrivacidadeUsuario, RecuperacaoSenha, Usuario, db
from models.tempo import utcnow
from PIL import Image
from services.conta.termos import VERSAO_TERMOS
from services.integracoes.enviar_email_service import EnviarEmailService


def imagem():
    buffer = io.BytesIO()
    Image.new("RGB", (30, 25), "purple").save(buffer, "PNG")
    buffer.seek(0)
    return buffer


class EmailTeste:
    def __init__(self):
        self.enviados = []

    def verificar_configuracao(self):
        return "https://momentus.example"

    def executar(self, destinatario, link):
        self.enviados.append((destinatario, link))


class PrivacidadeContaTest(unittest.TestCase):
    def setUp(self):
        self.pasta = tempfile.TemporaryDirectory()
        self.app = create_app(
            {
                "TESTING": True,
                "SECRET_KEY": "segredo-teste",
                "SQLALCHEMY_DATABASE_URI": "sqlite:///" + self.pasta.name + "/teste.db",
                "UPLOAD_FOLDER": self.pasta.name + "/uploads",
            }
        )
        self.cliente = self.app.test_client()
        self.email = EmailTeste()
        self.app.extensions["momentus"].email = self.email
        self.payload = {
            "faixa_etaria": "adulto",
            "declaracao_idade": True,
            "nome": "Pessoa Teste",
            "email": "pessoa@example.com",
            "senha": "senha-original",
            "aceite_termos": True,
            "versao_termos": VERSAO_TERMOS,
        }

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.engine.dispose()
        self.pasta.cleanup()

    def cadastrar(self, cliente=None, **alteracoes):
        return (cliente or self.cliente).post(
            "/auth/cadastro", json={**self.payload, **alteracoes}
        )

    def solicitar(self):
        return self.cliente.post(
            "/auth/recuperacao", json={"email": self.payload["email"]}
        )

    def token(self):
        return parse_qs(urlsplit(self.email.enviados[-1][1]).fragment)["token"][0]

    def test_cadastro_exige_aceite_explicito_e_versao_atual(self):
        for aceite in (False, "true", 1, None):
            self.assertEqual(self.cadastrar(aceite_termos=aceite).status_code, 400)
        self.assertEqual(self.cadastrar(versao_termos="antiga").status_code, 400)
        self.assertEqual(self.cadastrar().status_code, 201)
        info = self.cliente.get("/privacidade/info").get_json()
        self.assertEqual(info["aceite"]["versao"], VERSAO_TERMOS)
        self.assertTrue(info["aceite"]["aceito_em"].endswith("Z"))
        self.assertEqual(
            self.cliente.post("/privacidade/aceite", json=self.payload).get_json(),
            info["aceite"],
        )

    def test_conta_preexistente_nao_recebe_aceite_inventado(self):
        with self.app.app_context():
            usuario = Usuario(nome="Antigo", email=self.payload["email"])
            usuario.definir_senha("senha-original")
            usuario.salvar()
        self.cliente.post("/auth/login", json=self.payload)
        self.assertIsNone(self.cliente.get("/privacidade/info").get_json()["aceite"])
        self.assertEqual(
            self.cliente.post("/privacidade/aceite", json=self.payload).status_code, 200
        )

    def test_contato_configuravel_e_rotas_publicas(self):
        self.app.config.update(
            PRIVACY_CONTROLLER="Grupo Momentus", PRIVACY_EMAIL="contato@example.com"
        )
        info = self.cliente.get("/privacidade/info").get_json()
        self.assertEqual(info["responsavel"], "Grupo Momentus")
        self.assertEqual(info["email"], "contato@example.com")
        self.assertIsNone(info["aceite"])
        for pagina in (
            "termos.html",
            "privacidade.html",
            "recuperar-senha.html",
            "redefinir-senha.html",
            "documentos/modelo-termo-uso-professora.pdf",
        ):
            resposta = self.cliente.get("/" + pagina)
            self.assertEqual(resposta.status_code, 200, pagina)
            resposta.close()

    def test_avatar_valida_substitui_remove_e_protege(self):
        self.cadastrar()
        self.assertEqual(
            self.cliente.post(
                "/auth/foto", data={"foto": (io.BytesIO(b"invalido"), "foto.jpg")}
            ).status_code,
            400,
        )
        resposta = self.cliente.post(
            "/auth/foto", data={"foto": (imagem(), "meu-nome.png")}
        )
        self.assertEqual(resposta.status_code, 200)
        url = resposta.get_json()["usuario"]["foto_url"]
        self.assertNotIn("meu-nome", url)
        pasta = Path(self.app.config["UPLOAD_FOLDER"])
        with Image.open(pasta / url.rsplit("/", 1)[-1]) as avatar:
            self.assertEqual(avatar.format, "WEBP")
            self.assertFalse(avatar.getexif())
        resposta = self.cliente.get(url)
        self.assertEqual(resposta.status_code, 200)
        self.assertIn("no-store", resposta.headers["Cache-Control"])
        resposta.close()
        outro = self.app.test_client()
        self.assertEqual(outro.get(url).status_code, 401)
        self.cadastrar(outro, email="outro@example.com")
        self.assertEqual(outro.get(url).status_code, 404)
        self.cliente.post("/auth/foto", data={"foto": (imagem(), "outra.png")})
        self.assertFalse((pasta / url.rsplit("/", 1)[-1]).exists())
        self.assertEqual(self.cliente.delete("/auth/foto").status_code, 200)
        self.assertEqual(list(pasta.iterdir()), [])
        self.assertIsNone(
            self.cliente.get("/auth/me").get_json()["usuario"]["foto_url"]
        )

    def test_avatar_reverte_arquivo_se_commit_falhar(self):
        self.cadastrar()
        with patch.object(
            self.app.extensions["momentus"].transacao,
            "confirmar",
            side_effect=RuntimeError("falha"),
        ):
            with self.assertRaises(RuntimeError):
                self.cliente.post("/auth/foto", data={"foto": (imagem(), "foto.png")})
        self.assertEqual(list(Path(self.app.config["UPLOAD_FOLDER"]).iterdir()), [])

    def test_exportacao_nao_vaza_hash_tokens_nem_outros_usuarios(self):
        self.cadastrar()
        outro = self.app.test_client()
        self.cadastrar(outro, email="segredo@example.com")
        self.solicitar()
        resposta = self.cliente.get("/privacidade/meus-dados")
        self.assertEqual(resposta.status_code, 200)
        dados = resposta.get_json()
        self.assertEqual(dados["conta"]["email"], self.payload["email"])
        self.assertNotIn("senha_hash", resposta.text)
        self.assertNotIn(self.token(), resposta.text)
        self.assertNotIn("segredo@example.com", resposta.text)
        self.assertIn("no-store", resposta.headers["Cache-Control"])
        self.assertEqual(
            self.app.test_client().get("/privacidade/meus-dados").status_code, 401
        )

    def test_recuperacao_nao_revela_cadastro_e_limita_envios(self):
        self.cadastrar()
        resposta = self.solicitar()
        self.assertEqual(resposta.status_code, 200)
        desconhecido = self.cliente.post(
            "/auth/recuperacao", json={"email": "inexistente@example.com"}
        )
        self.assertEqual(resposta.get_json(), desconhecido.get_json())
        for _ in range(5):
            self.solicitar()
        self.assertEqual(len(self.email.enviados), 3)
        self.assertNotIn(self.token(), resposta.text)
        with self.app.app_context():
            self.assertNotEqual(RecuperacaoSenha.listar()[0].token_hash, self.token())

    def test_redefinir_invalida_sessao_antiga_e_link_usado(self):
        self.cadastrar()
        outra_sessao = self.app.test_client()
        outra_sessao.post("/auth/login", json=self.payload)
        self.solicitar()
        token = self.token()
        self.assertEqual(
            self.cliente.post(
                "/auth/redefinir-senha", json={"token": token, "senha": "senha-nova"}
            ).status_code,
            200,
        )
        self.assertEqual(outra_sessao.get("/auth/me").status_code, 401)
        self.assertEqual(
            self.cliente.post(
                "/auth/redefinir-senha", json={"token": token, "senha": "outra-senha"}
            ).status_code,
            400,
        )
        self.assertEqual(
            self.cliente.post("/auth/login", json=self.payload).status_code, 401
        )
        self.assertEqual(
            self.cliente.post(
                "/auth/login", json={**self.payload, "senha": "senha-nova"}
            ).status_code,
            200,
        )

    def test_expiracao_link_substituido_email_alterado_e_senha_invalida(self):
        self.cadastrar()
        self.solicitar()
        antigo = self.token()
        self.solicitar()
        token = self.token()
        self.assertEqual(
            self.cliente.post(
                "/auth/redefinir-senha", json={"token": antigo, "senha": "senha-nova"}
            ).status_code,
            400,
        )
        self.assertEqual(
            self.cliente.post(
                "/auth/redefinir-senha", json={"token": token, "senha": "curta"}
            ).status_code,
            400,
        )
        with self.app.app_context():
            for item in RecuperacaoSenha.listar():
                item.expira_em = utcnow() - timedelta(seconds=1)
            db.session.commit()
        self.assertEqual(
            self.cliente.post(
                "/auth/redefinir-senha", json={"token": token, "senha": "senha-nova"}
            ).status_code,
            400,
        )
        self.solicitar()
        token = self.token()
        self.cliente.put("/auth/perfil", json={"email": "alterado@example.com"})
        self.assertEqual(
            self.cliente.post(
                "/auth/redefinir-senha", json={"token": token, "senha": "senha-nova"}
            ).status_code,
            400,
        )

    def test_smtp_ausente_exibe_erro_real(self):
        self.app.extensions["momentus"].email = EnviarEmailService({})
        resposta = self.solicitar()
        self.assertEqual(resposta.status_code, 502)
        self.assertIn("não foi configurada", resposta.get_json()["erro"])

    def test_envio_falha_sem_deixar_token_novo(self):
        self.cadastrar()
        with patch.object(
            self.email, "executar", side_effect=IntegracaoIndisponivel("falha")
        ):
            self.assertEqual(self.solicitar().status_code, 502)
        with self.app.app_context():
            self.assertEqual(RecuperacaoSenha.listar(), [])

    def test_smtp_usa_tls_e_origem_configurada(self):
        config = {
            "PUBLIC_BASE_URL": "https://momentus.example",
            "SMTP_HOST": "smtp.example",
            "SMTP_FROM": "contato@example.com",
            "SMTP_USERNAME": "usuario",
            "SMTP_PASSWORD": "segredo",
        }
        with patch("services.integracoes.enviar_email_service.smtplib.SMTP") as smtp:
            EnviarEmailService(config).executar(
                "pessoa@example.com",
                "https://momentus.example/redefinir-senha.html#token=teste",
            )
            conexao = smtp.return_value.__enter__.return_value
            conexao.starttls.assert_called_once()
            conexao.login.assert_called_once_with("usuario", "segredo")
            conexao.send_message.assert_called_once()
        for origem in (
            "http://site-publico.example",
            "https://usuario:senha@site.example",
            "javascript:alert(1)",
        ):
            with self.assertRaises(IntegracaoIndisponivel):
                EnviarEmailService(
                    {**config, "PUBLIC_BASE_URL": origem}
                ).verificar_configuracao()

    def test_excluir_conta_apaga_avatar_tokens_e_aceite(self):
        self.cadastrar()
        self.solicitar()
        self.cliente.post("/auth/foto", data={"foto": (imagem(), "foto.png")})
        self.assertEqual(self.cliente.delete("/auth/conta").status_code, 204)
        with self.app.app_context():
            self.assertEqual(PrivacidadeUsuario.listar(), [])
            self.assertEqual(RecuperacaoSenha.listar(), [])
        self.assertEqual(list(Path(self.app.config["UPLOAD_FOLDER"]).iterdir()), [])

    def test_uploads_exigem_acesso_ao_evento_e_revogacao_e_imediata(self):
        self.cadastrar()
        evento = self.cliente.post(
            "/eventos",
            json={
                "nome_evento": "Evento privado",
                "tipo_evento": "aniversario",
                "data_evento": "2030-10-28",
                "cidade_evento": "Belo Horizonte",
                "orcamento_evento": 100,
            },
        ).get_json()
        base = "/eventos/" + str(evento["id"])
        foto = self.cliente.post(
            base + "/fotos", data={"foto": (imagem(), "foto.png")}
        ).get_json()
        outro = self.app.test_client()
        self.cadastrar(outro, email="outro@example.com")
        self.assertEqual(outro.get(foto["url"]).status_code, 404)
        colaborador = self.cliente.post(
            base + "/colaboradores",
            json={"nome": "Outra pessoa", "email": "outro@example.com"},
        ).get_json()
        self.assertEqual(outro.get(foto["url"]).status_code, 404)
        outro.post(
            "/colaboracoes/" + colaborador["token"] + "/responder",
            json={"status": "ativo"},
        )
        resposta = outro.get(foto["url"])
        self.assertEqual(resposta.status_code, 200)
        resposta.close()
        self.cliente.delete(base + "/colaboradores/" + colaborador["id"])
        self.assertEqual(outro.get(foto["url"]).status_code, 404)
        self.assertEqual(self.app.test_client().get(foto["url"]).status_code, 401)

    def test_banco_antigo_recebe_tabelas_sem_apagar_contas(self):
        import sqlite3

        arquivo = Path(self.pasta.name) / "anterior.db"
        # Tabela de contas do esquema anterior, sem as novas tabelas de apoio.
        with sqlite3.connect(arquivo) as conn:
            conn.execute(
                "CREATE TABLE usuarios (id INTEGER PRIMARY KEY, nome VARCHAR(160) NOT NULL, email VARCHAR(180) UNIQUE NOT NULL, telefone VARCHAR(40), senha_hash VARCHAR(255) NOT NULL, tipo VARCHAR(30) NOT NULL, ativo BOOLEAN NOT NULL, criado_em DATETIME NOT NULL)"
            )
            conn.execute(
                "INSERT INTO usuarios (nome, email, senha_hash, tipo, ativo, criado_em) VALUES ('Conta anterior', 'anterior@example.com', 'hash', 'cliente', 1, '2026-10-01 00:00:00')"
            )
        app = create_app(
            {
                "TESTING": True,
                "SQLALCHEMY_DATABASE_URI": "sqlite:///" + str(arquivo),
                "UPLOAD_FOLDER": self.pasta.name + "/uploads2",
            }
        )
        with app.app_context():
            try:
                self.assertIsNotNone(Usuario.buscar_um(email="anterior@example.com"))
                self.assertEqual(PrivacidadeUsuario.listar(), [])
                self.assertEqual(RecuperacaoSenha.listar(), [])
            finally:
                db.session.remove()
                db.engine.dispose()
