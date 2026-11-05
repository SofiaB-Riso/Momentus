"""Regressões dos achados: permissões, consentimentos e integridade dos envios."""

import io
import os
import tempfile
import unittest
from datetime import date, timedelta
from pathlib import Path
from urllib.parse import parse_qs, urlsplit
from uuid import uuid4

os.environ["DATABASE_URL"] = "sqlite://"
from app import create_app
from models import (
    AutorizacaoConta,
    ColaboradorEvento,
    Convidado,
    DespesaEvento,
    Usuario,
    db,
)
from PIL import Image


class CorrecoesAuditoriaTest(unittest.TestCase):
    def setUp(self):
        self.pasta = tempfile.TemporaryDirectory()
        self.app = create_app(
            {
                "TESTING": True,
                "SECRET_KEY": "teste-isolado",
                "SQLALCHEMY_DATABASE_URI": "sqlite:///" + self.pasta.name + "/teste.db",
                "UPLOAD_FOLDER": self.pasta.name + "/uploads",
                "LIVE_INTERVAL": 0,
                "LIVE_ITERATIONS": 1,
            }
        )
        self.dono = self.app.test_client()
        self.cadastrar(self.dono, "dono@teste.example")
        self.base = "/eventos/" + str(self.evento(self.dono))

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.engine.dispose()
        self.pasta.cleanup()

    def cadastrar(self, cliente, email, faixa="adulto"):
        r = cliente.post(
            "/auth/cadastro",
            json={
                "nome": "Pessoa Teste",
                "email": email,
                "senha": "senha-teste",
                "aceite_termos": True,
                "versao_termos": "2026-10-30",
                "faixa_etaria": faixa,
                "declaracao_idade": True,
            },
        )
        self.assertEqual(r.status_code, 201, r.get_json())
        return r.get_json()["usuario"]["id"]

    def evento(self, cliente, **campos):
        r = cliente.post(
            "/eventos",
            json={
                "nome_evento": "Evento Teste",
                "tipo_evento": "Aniversário",
                "data_evento": (date.today() + timedelta(days=1)).isoformat(),
                **campos,
            },
        )
        self.assertEqual(r.status_code, 201, r.get_json())
        return r.get_json()["id"]

    def convidado(self):
        r = self.dono.post(self.base + "/convidados", json={"nome": "Pessoa convidada"})
        self.assertEqual(r.status_code, 201, r.get_json())
        return r.get_json()

    def responsavel(self, link, **campos):
        segredo = {k: v[0] for k, v in parse_qs(urlsplit(link).fragment).items()}
        return self.app.test_client().post(
            "/autorizacoes/responder",
            json={
                **segredo,
                "responsavel_nome": "Responsável Teste",
                "responsavel_email": "responsavel@teste.example",
                "vinculo": "Mãe",
                "declaracao_responsavel": True,
                "versao_consentimento": "2026-10-30",
                **campos,
            },
        )

    def test_comprovante_nao_aceita_referencia_arbitraria(self):
        r = self.dono.post(
            self.base + "/despesas",
            json={
                "descricao": "Compra",
                "valor": 10,
                "comprovante": "outro-arquivo.png",
            },
        )
        self.assertEqual(r.status_code, 400)
        self.assertEqual(self.dono.get(self.base + "/despesas").get_json(), [])

    def test_referencia_legada_nao_apaga_foto_de_outro_evento(self):
        imagem = io.BytesIO()
        Image.new("RGB", (16, 16), "purple").save(imagem, "PNG")
        imagem.seek(0)
        foto = self.dono.post(
            self.base + "/fotos", data={"foto": (imagem, "imagem.png")}
        ).get_json()
        outro = self.app.test_client()
        ident = self.cadastrar(outro, "outro@teste.example")
        outro_evento = self.evento(outro)
        with self.app.app_context():
            despesa = DespesaEvento(
                evento_id=outro_evento,
                descricao="Vínculo antigo inválido",
                valor=1,
                comprovante=foto["url"].split("/")[-1],
            ).salvar()
            despesa_id = despesa.id
        self.assertEqual(
            outro.delete(f"/eventos/{outro_evento}/despesas/{despesa_id}").status_code,
            204,
        )
        self.assertTrue(
            (Path(self.pasta.name) / "uploads" / foto["url"].split("/")[-1]).exists()
        )
        self.assertEqual(self.dono.get(foto["url"]).status_code, 200)
        self.assertGreater(ident, 0)

    def test_despesa_reenvio_idempotente_e_payload_diferente(self):
        headers = {"Idempotency-Key": str(uuid4())}
        dados = {"descricao": "Bolo", "valor": "12.35"}
        a = self.dono.post(self.base + "/despesas", json=dados, headers=headers)
        b = self.dono.post(self.base + "/despesas", json=dados, headers=headers)
        self.assertEqual((a.status_code, b.status_code), (201, 201))
        self.assertEqual(a.json["despesa"]["id"], b.json["despesa"]["id"])
        self.assertEqual(len(self.dono.get(self.base + "/despesas").json), 1)
        self.assertEqual(
            self.dono.post(
                self.base + "/despesas", json={**dados, "valor": 99}, headers=headers
            ).status_code,
            409,
        )

    def test_reenvio_despesa_excluida_nao_recria_lancamento(self):
        h = {"Idempotency-Key": str(uuid4())}
        p = {"descricao": "Despesa", "valor": 5}
        criada = self.dono.post(self.base + "/despesas", json=p, headers=h).json[
            "despesa"
        ]
        self.assertEqual(
            self.dono.delete(self.base + "/despesas/" + criada["id"]).status_code, 204
        )
        self.assertEqual(
            self.dono.post(self.base + "/despesas", json=p, headers=h).status_code, 409
        )

    def test_despesa_concorrente_com_mesma_chave_cria_um_registro(self):
        from concurrent.futures import ThreadPoolExecutor
        from threading import Barrier

        barreira = Barrier(2)
        cookie = self.dono.get_cookie("session").value
        chave = str(uuid4())

        def enviar():
            cliente = self.app.test_client()
            cliente.set_cookie("session", cookie)
            barreira.wait(timeout=10)
            resposta = cliente.post(
                self.base + "/despesas",
                json={"descricao": "Envio concorrente", "valor": 30},
                headers={"Idempotency-Key": chave},
            )
            return resposta.status_code, resposta.get_json()

        with ThreadPoolExecutor(max_workers=2) as executor:
            respostas = list(executor.map(lambda _: enviar(), range(2)))
        self.assertEqual([r[0] for r in respostas], [201, 201], respostas)
        self.assertEqual(
            respostas[0][1]["despesa"]["id"], respostas[1][1]["despesa"]["id"]
        )
        self.assertEqual(len(self.dono.get(self.base + "/despesas").json), 1)

    def test_json_invalido_retorna_400_sem_alterar_evento(self):
        for valor in [[], "texto", 7, None]:
            with self.subTest(valor=valor):
                self.assertEqual(
                    self.dono.put(
                        self.base,
                        data=__import__("json").dumps(valor),
                        content_type="application/json",
                    ).status_code,
                    400,
                )
        self.assertEqual(self.dono.get(self.base).json["nome_evento"], "Evento Teste")

    def test_email_sem_link_nao_recebe_ou_aceita_convite(self):
        convite = self.dono.post(
            self.base + "/colaboradores",
            json={"nome": "Nova Pessoa", "email": "nova@teste.example"},
        ).json
        nova = self.app.test_client()
        self.cadastrar(nova, "nova@teste.example")
        self.assertEqual(nova.get("/notificacoes").json, [])
        self.assertEqual(
            nova.put(
                self.base + "/colaboradores/" + convite["id"], json={"status": "ativo"}
            ).status_code,
            403,
        )
        self.assertEqual(nova.get(self.base).status_code, 403)
        self.assertEqual(
            nova.post(
                "/colaboracoes/" + convite["token"] + "/responder",
                json={"status": "ativo"},
            ).status_code,
            200,
        )
        self.assertEqual(nova.get(self.base).status_code, 200)

    def test_convite_aceito_fica_vinculado_a_conta_original(self):
        pessoa = self.app.test_client()
        self.cadastrar(pessoa, "pessoa@teste.example")
        convite = self.dono.post(
            self.base + "/colaboradores",
            json={"nome": "Pessoa", "email": "pessoa@teste.example"},
        ).json
        pessoa.post(
            "/colaboracoes/" + convite["token"] + "/responder", json={"status": "ativo"}
        )
        pessoa.put("/auth/perfil", json={"email": "novo@teste.example"})
        outra = self.app.test_client()
        self.cadastrar(outra, "pessoa@teste.example")
        self.assertEqual(
            outra.post(
                "/colaboracoes/" + convite["token"] + "/responder",
                json={"status": "ativo"},
            ).status_code,
            403,
        )

    def test_progresso_ao_inserir_tarefa_pendente(self):
        for t in self.dono.get(self.base).json["tarefas"]:
            self.dono.put(self.base + "/tarefas/" + t["id"], json={"feita": True})
        self.assertEqual(self.dono.get(self.base).json["progresso"], 100)
        self.dono.post(self.base + "/tarefas", json={"titulo": "Mais uma tarefa"})
        self.assertEqual(self.dono.get(self.base).json["progresso"], 80)

    def test_rascunho_nao_gera_lembretes(self):
        ident = self.evento(self.dono, status="rascunho")
        self.assertFalse(
            any(
                n["eventoId"] == str(ident) for n in self.dono.get("/notificacoes").json
            )
        )

    def test_preferencias_persistem_e_filtram_rsvp(self):
        c = self.convidado()
        self.assertEqual(
            self.dono.put(
                "/privacidade/preferencias", json={"rsvp": False, "lembretes": False}
            ).status_code,
            200,
        )
        self.app.test_client().post(
            "/rsvp/" + c["token_rsvp"], json={"status": "confirmado"}
        )
        self.assertFalse(
            any(
                n["tipo"] == "rsvp" or n["tipo"].startswith("lembrete-")
                for n in self.dono.get("/notificacoes").json
            )
        )
        novo = self.app.test_client()
        novo.post(
            "/auth/login", json={"email": "dono@teste.example", "senha": "senha-teste"}
        )
        self.assertEqual(
            novo.get("/auth/me").json["usuario"]["preferencias"],
            {"rsvp": False, "lembretes": False},
        )

    def test_preferencia_invalida_nao_e_persistida(self):
        self.assertEqual(
            self.dono.put(
                "/privacidade/preferencias", json={"rsvp": "false"}
            ).status_code,
            400,
        )
        self.assertTrue(
            self.dono.get("/auth/me").json["usuario"]["preferencias"]["rsvp"]
        )

    def test_valores_invalidos_recebem_400_sem_gravar(self):
        for dados in [
            {"convidados_estimados": [1]},
            {"progresso": {"x": 1}},
            {"dados_evento": {"x": 1}},
            {"status": "inexistente"},
            {"nome_evento": " "},
            {"convidados_estimados": True},
        ]:
            with self.subTest(dados=dados):
                self.assertEqual(self.dono.put(self.base, json=dados).status_code, 400)
        self.assertEqual(self.dono.get(self.base).json["nome_evento"], "Evento Teste")

    def test_perfil_valida_nome_email_telefone_e_reverte(self):
        for dados in [
            {"email": "@"},
            {"email": "a b@c.example"},
            {"nome": "X"},
            {"nome": "  "},
            {"telefone": 123},
        ]:
            with self.subTest(dados=dados):
                self.assertEqual(
                    self.dono.put("/auth/perfil", json=dados).status_code, 400
                )
        self.assertEqual(
            self.dono.get("/auth/me").json["usuario"]["email"], "dono@teste.example"
        )

    def test_cadastro_exige_declaracao_de_idade(self):
        r = self.app.test_client().post(
            "/auth/cadastro",
            json={
                "nome": "Teste",
                "email": "idade@teste.example",
                "senha": "senha-teste",
                "aceite_termos": True,
                "versao_termos": "2026-10-30",
            },
        )
        self.assertEqual(r.status_code, 400)

    def test_autorizacao_recusa_tipo_e_faixa_etaria_compostos(self):
        self.assertEqual(
            self.dono.put(
                "/privacidade/autorizacao",
                json={"faixa_etaria": [], "declaracao_idade": True},
            ).status_code,
            400,
        )
        visitante = self.app.test_client()
        for rota in ["/autorizacoes/consultar", "/autorizacoes/responder"]:
            self.assertEqual(
                visitante.post(rota, json={"tipo": [], "token": "x" * 40}).status_code,
                400,
            )

    def test_menor_aguarda_responsavel_e_pode_revogar(self):
        menor = self.app.test_client()
        self.cadastrar(menor, "menor@teste.example", "menor")
        self.assertEqual(menor.get("/eventos").status_code, 403)
        self.assertEqual(menor.get("/auth/me").status_code, 200)
        link = menor.post("/privacidade/autorizacao/link").json["link"]
        self.assertEqual(self.responsavel(link, autorizar_conta=True).status_code, 200)
        self.assertEqual(menor.get("/eventos").status_code, 200)
        self.assertEqual(self.responsavel(link, autorizar_conta=True).status_code, 404)
        self.assertEqual(menor.delete("/privacidade/autorizacao").status_code, 200)
        self.assertEqual(menor.get("/eventos").status_code, 403)

    def test_responsavel_pode_negar_conta(self):
        menor = self.app.test_client()
        self.cadastrar(menor, "negado@teste.example", "menor")
        link = menor.post("/privacidade/autorizacao/link").json["link"]
        self.assertEqual(self.responsavel(link, autorizar_conta=False).status_code, 200)
        self.assertEqual(menor.get("/privacidade/autorizacao").json["status"], "negado")
        self.assertEqual(menor.get("/eventos").status_code, 403)

    def test_link_responsavel_expira_e_novo_invalida_anterior(self):
        menor = self.app.test_client()
        uid = self.cadastrar(menor, "expira@teste.example", "menor")
        antigo = menor.post("/privacidade/autorizacao/link").json["link"]
        novo = menor.post("/privacidade/autorizacao/link").json["link"]
        self.assertEqual(
            self.responsavel(antigo, autorizar_conta=True).status_code, 404
        )
        with self.app.app_context():
            AutorizacaoConta.buscar_por_id(uid).expira_em = date.today() - timedelta(
                days=1
            )
            db.session.commit()
        self.assertEqual(self.responsavel(novo, autorizar_conta=True).status_code, 404)

    def test_conta_legada_deve_declarar_idade_sem_aceite_inventado(self):
        with self.app.app_context():
            u = Usuario(nome="Conta antiga", email="antiga@teste.example")
            u.definir_senha("senha-teste")
            u.salvar()
        c = self.app.test_client()
        c.post(
            "/auth/login",
            json={"email": "antiga@teste.example", "senha": "senha-teste"},
        )
        self.assertEqual(c.get("/eventos").status_code, 403)
        self.assertIsNone(c.get("/privacidade/info").json["aceite"])
        self.assertEqual(
            c.put(
                "/privacidade/autorizacao",
                json={"faixa_etaria": "adulto", "declaracao_idade": True},
            ).status_code,
            200,
        )
        self.assertEqual(c.get("/eventos").status_code, 200)

    def test_saude_exige_consentimento_especifico_e_adulto(self):
        c = self.convidado()
        rota = "/rsvp/" + c["token_rsvp"]
        payload = {
            "status": "confirmado",
            "saude": "Alergia de teste",
            "faixa_etaria": "adulto",
        }
        self.assertEqual(
            self.app.test_client().post(rota, json=payload).status_code, 400
        )
        r = self.app.test_client().post(
            rota,
            json={
                **payload,
                "autorizar_saude": True,
                "versao_consentimento": "2026-10-30",
            },
        )
        self.assertEqual(r.status_code, 200, r.json)
        self.assertEqual(
            self.dono.get(self.base).json["lista_convidados"][0]["informacoes_saude"],
            "Alergia de teste",
        )
        self.assertEqual(
            self.app.test_client()
            .post(rota, json={"status": "confirmado", "revogar_saude": True})
            .status_code,
            200,
        )
        self.assertEqual(
            self.dono.get(self.base).json["lista_convidados"][0]["informacoes_saude"],
            "",
        )

    def test_organizador_nao_fornece_saude_por_terceiro(self):
        r = self.dono.post(
            self.base + "/convidados",
            json={
                "nome": "Terceiro",
                "saude": "Alergia",
                "autorizar_saude": True,
                "versao_consentimento": "2026-10-30",
            },
        )
        self.assertEqual(r.status_code, 400)
        self.assertEqual(self.dono.get(self.base).json["lista_convidados"], [])

    def test_preferencias_exigem_declaracao_e_nao_substituem_saude(self):
        self.assertEqual(
            self.dono.post(
                self.base + "/convidados",
                json={"nome": "Teste", "restricoes": "Vegetariano"},
            ).status_code,
            400,
        )
        r = self.dono.post(
            self.base + "/convidados",
            json={
                "nome": "Teste",
                "restricoes": "Vegetariano",
                "preferencias_sem_saude": True,
            },
        )
        self.assertEqual(r.status_code, 201)
        self.assertEqual(r.json["preferencias_alimentares"], "Vegetariano")
        self.assertFalse(r.json["consentimento"]["autorizado"])

    def test_dados_alimentares_antigos_aguardam_reclassificacao(self):
        with self.app.app_context():
            Convidado(
                evento_id=int(self.base.split("/")[-1]),
                nome="Antigo",
                restricoes_alimentares="Informação anterior não classificada",
            ).salvar()
        convidado = self.dono.get(self.base).json["lista_convidados"][0]
        self.assertTrue(convidado["dados_anteriores_pendentes"])
        self.assertEqual(convidado["restricoes"], "")
        self.assertNotIn(
            "Informação anterior",
            self.dono.get(self.base + "/resumo").get_data(as_text=True),
        )

    def test_saude_menor_depende_de_responsavel_e_participacao(self):
        c = self.convidado()
        rota = "/rsvp/" + c["token_rsvp"]
        visitante = self.app.test_client()
        link = visitante.post(rota + "/responsavel").json["link"]
        self.assertEqual(
            visitante.post(rota, json={"status": "confirmado"}).status_code, 400
        )
        self.assertEqual(
            self.responsavel(
                link,
                autorizar_participacao=True,
                autorizar_saude=True,
                saude="Cuidado alimentar de teste",
            ).status_code,
            200,
        )
        self.assertEqual(
            visitante.post(rota, json={"status": "confirmado"}).status_code, 200
        )
        self.assertEqual(
            visitante.get(rota).json["convidado"]["informacoes_saude"],
            "Cuidado alimentar de teste",
        )
        visitante.post(rota, json={"status": "confirmado", "revogar_saude": True})
        self.assertEqual(visitante.get(rota).json["convidado"]["informacoes_saude"], "")

    def test_exclusao_anonimiza_colaboracao_e_invalida_link(self):
        pessoa = self.app.test_client()
        self.cadastrar(pessoa, "excluir@teste.example")
        convite = self.dono.post(
            self.base + "/colaboradores",
            json={"nome": "Nome identificável", "email": "excluir@teste.example"},
        ).json
        pessoa.post(
            "/colaboracoes/" + convite["token"] + "/responder", json={"status": "ativo"}
        )
        self.assertEqual(pessoa.delete("/auth/conta").status_code, 204)
        with self.app.app_context():
            registro = ColaboradorEvento.buscar_por_id(convite["id"])
            self.assertEqual(registro.email, "")
            self.assertEqual(registro.nome, "Participante excluído")
            self.assertIsNone(registro.usuario_id)
        self.assertEqual(
            self.app.test_client().get("/colaboracoes/" + convite["token"]).status_code,
            404,
        )


class SegurancaHTTPTest(unittest.TestCase):
    def setUp(self):
        self.app = create_app(
            {
                "TESTING": True,
                "SECRET_KEY": "teste-seguranca",
                "SQLALCHEMY_DATABASE_URI": "sqlite://",
                "CSRF_ENABLED": True,
            }
        )
        self.c = self.app.test_client()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.engine.dispose()

    def test_csrf_e_origem(self):
        self.assertEqual(self.c.post("/auth/logout").status_code, 403)
        token = self.c.get("/auth/csrf").json["token"]
        self.assertEqual(
            self.c.post(
                "/auth/logout",
                headers={"X-CSRF-Token": token, "Origin": "https://outro.example"},
            ).status_code,
            403,
        )
        self.assertEqual(
            self.c.post(
                "/auth/logout",
                headers={"X-CSRF-Token": token, "Origin": "http://localhost"},
            ).status_code,
            204,
        )

    def test_limite_login_nao_revela_email(self):
        self.app.config.update(CSRF_ENABLED=False, RATE_LIMIT_ENABLED=True)
        for _ in range(10):
            self.assertEqual(
                self.c.post(
                    "/auth/login",
                    json={"email": "inexistente@teste.example", "senha": "errada"},
                ).status_code,
                401,
            )
        r = self.c.post(
            "/auth/login",
            json={"email": "inexistente@teste.example", "senha": "errada"},
        )
        self.assertEqual(r.status_code, 429)
        self.assertIn("Retry-After", r.headers)

    def test_csrf_autenticado_estavel_sem_regravar_cookie_em_leituras(self):
        token = self.c.get("/auth/csrf").json["token"]
        resposta = self.c.post(
            "/auth/cadastro",
            json={
                "nome": "Pessoa Teste",
                "email": "csrf@teste.example",
                "senha": "senha-teste",
                "aceite_termos": True,
                "versao_termos": "2026-10-30",
                "faixa_etaria": "adulto",
                "declaracao_idade": True,
            },
            headers={"X-CSRF-Token": token},
        )
        self.assertEqual(resposta.status_code, 201)
        token = self.c.get("/auth/csrf").json["token"]
        for rota in ["/auth/me", "/eventos", "/auth/csrf", "/notificacoes"]:
            r = self.c.get(rota)
            self.assertEqual(r.status_code, 200)
            self.assertNotIn("Set-Cookie", r.headers)
        self.assertEqual(self.c.get("/auth/csrf").json["token"], token)
        self.assertEqual(
            self.c.post("/auth/logout", headers={"X-CSRF-Token": token}).status_code,
            204,
        )
        self.assertEqual(
            self.c.post("/auth/logout", headers={"X-CSRF-Token": token}).status_code,
            403,
        )

    def test_configuracao_producao_recusa_segredo_fraco(self):
        with self.assertRaises(RuntimeError):
            create_app(
                {
                    "APP_ENV": "production",
                    "SECRET_KEY": "troque-chave",
                    "SQLALCHEMY_DATABASE_URI": "sqlite://",
                }
            )

    def test_cabecalhos_e_csp(self):
        r = self.c.get("/auth/csrf")
        self.assertIn("no-store", r.headers["Cache-Control"])
        self.assertEqual(r.headers["X-Content-Type-Options"], "nosniff")
        self.assertEqual(r.headers["X-Frame-Options"], "DENY")
        self.assertIn("script-src 'self'", r.headers["Content-Security-Policy"])
