"""Fluxos reais da API; banco temporário, sem chamadas externas nem dados pessoais."""

import os
import sys
import tempfile
import unittest
from concurrent.futures import ThreadPoolExecutor
from datetime import date, timedelta
from pathlib import Path
from threading import Barrier
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
os.environ["DATABASE_URL"] = "sqlite://"
from app import create_app
from infrastructure.provedores.google_places import GooglePlacesIndisponivel
from models import ColaboradorEvento, Evento, db


class ColaboracaoTest(unittest.TestCase):
    def setUp(self):
        self.pasta = tempfile.TemporaryDirectory(prefix="momentus-test-")
        self.app = create_app(
            {
                "TESTING": True,
                "SECRET_KEY": "chave-apenas-de-teste",
                "SQLALCHEMY_DATABASE_URI": "sqlite:///"
                + str(Path(self.pasta.name) / "teste.db"),
                "LIVE_INTERVAL": 0,
                "LIVE_ITERATIONS": 2,
            }
        )
        self.dono = self.app.test_client()
        self.editor = self.app.test_client()
        self.leitor = self.app.test_client()
        self.visitante = self.app.test_client()
        for cliente, nome in (
            (self.dono, "Organizadora"),
            (self.editor, "Colaborador"),
            (self.leitor, "Leitora"),
        ):
            resposta = cliente.post(
                "/auth/cadastro",
                json={
                    "nome": nome,
                    "email": nome.lower() + "@teste.example",
                    "senha": "senha-teste-123",
                },
            )
            self.assertEqual(resposta.status_code, 201)
        self.evento = self.dono.post(
            "/eventos",
            json={
                "nome_evento": "Festa de teste",
                "tipo_evento": "aniversario",
                "data_evento": (date.today() + timedelta(days=1)).isoformat(),
                "cidade_evento": "São Paulo",
                "endereco_evento": "Rua A & B, 123",
                "estilo_evento": "rústico",
                "convidados_estimados": 30,
                "orcamento_evento": 3000,
            },
        ).get_json()
        self.id = self.evento["id"]
        self.base = f"/eventos/{self.id}"
        self.colab = self.dono.post(
            self.base + "/colaboradores",
            json={"nome": "Colaborador", "email": "colaborador@teste.example"},
        ).get_json()
        self.editor.post(
            "/colaboracoes/" + self.colab["token"] + "/responder",
            json={"status": "ativo"},
        )
        self.view = self.dono.post(
            self.base + "/colaboradores",
            json={
                "nome": "Leitora",
                "email": "leitora@teste.example",
                "pode_editar": False,
            },
        ).get_json()
        self.leitor.post(
            "/colaboracoes/" + self.view["token"] + "/responder",
            json={"status": "ativo"},
        )
        self.g1 = self.dono.post(
            self.base + "/convidados",
            json={"nome": "Ana", "email": "ana@teste.example"},
        ).get_json()
        self.g2 = self.dono.post(
            self.base + "/convidados", json={"nome": "Bruna"}
        ).get_json()
        self.r1 = "/rsvp/" + self.g1["token_rsvp"]
        self.r2 = "/rsvp/" + self.g2["token_rsvp"]

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.engine.dispose()
        self.pasta.cleanup()

    def item(self, nome="Refrigerante"):
        r = self.dono.post(
            self.base + "/itens-compartilhados", json={"nome": nome, "quantidade": 3}
        )
        self.assertEqual(r.status_code, 201, r.get_json())
        return r.get_json()["id"]

    def test_reserva_exclusiva_quantidade_e_privacidade(self):
        item = self.item()
        self.assertEqual(
            self.visitante.post(f"{self.r1}/itens/{item}/assumir").status_code, 200
        )
        self.assertEqual(
            self.visitante.post(f"{self.r2}/itens/{item}/assumir").status_code, 409
        )
        self.assertEqual(
            self.visitante.post(f"{self.r2}/itens/{item}/liberar").status_code, 403
        )
        publico = self.visitante.get(self.r2).get_json()
        self.assertEqual(
            publico["evento"]["itens_compartilhados"][0]["responsavelNome"],
            "Já reservado",
        )
        self.assertNotIn("token_rsvp", publico["convidado"])
        self.assertEqual(publico["evento"]["confirmados_publicos"], [])
        privado = self.dono.get(self.base).get_json()["itens_compartilhados"][0]
        self.assertEqual(
            (privado["responsavelNome"], privado["quantidade"]), ("Ana", 3)
        )

    def test_concorrencia_reserva(self):
        item = self.item()
        barreira = Barrier(2)

        def reservar(url):
            cliente = self.app.test_client()
            barreira.wait()
            return cliente.post(f"{url}/itens/{item}/assumir").status_code

        with ThreadPoolExecutor(max_workers=2) as executor:
            resultados = list(executor.map(reservar, [self.r1, self.r2]))
        self.assertEqual(sorted(resultados), [200, 409])

    def test_duplicatas_normalizadas_e_quantidade_invalida(self):
        self.item("  Pão   de queijo ")
        r = self.dono.post(
            self.base + "/itens-compartilhados",
            json={"nome": "pao de  QUEIJO", "quantidade": 1},
        )
        self.assertEqual(r.status_code, 409)
        for valor in (0, -1, 1.5, "abc", None):
            self.assertEqual(
                self.dono.post(
                    self.base + "/itens-compartilhados",
                    json={"nome": "Novo", "quantidade": valor},
                ).status_code,
                400,
            )

    def test_recusa_e_remocao_liberam_itens(self):
        item = self.item()
        self.visitante.post(f"{self.r1}/itens/{item}/assumir")
        self.assertEqual(
            self.visitante.post(
                self.r1, json={"status": "recusado", "restricoes": "alergia a amendoim"}
            ).status_code,
            200,
        )
        self.assertFalse(
            self.dono.get(self.base).get_json()["itens_compartilhados"][0][
                "responsavelNome"
            ]
        )
        self.assertEqual(
            self.visitante.post(f"{self.r1}/itens/{item}/assumir").status_code, 400
        )
        self.visitante.post(f"{self.r2}/itens/{item}/assumir")
        self.dono.delete(self.base + "/convidados/" + self.g2["id"])
        self.assertFalse(
            self.dono.get(self.base).get_json()["itens_compartilhados"][0][
                "responsavelNome"
            ]
        )

    def test_alergias_presenca_e_notificacoes_integradas(self):
        for status in ("confirmado", "pendente", "recusado"):
            self.assertEqual(
                self.visitante.post(
                    self.r1,
                    json={"status": status, "restricoes": "Alergia a castanhas"},
                ).status_code,
                200,
            )
        self.visitante.post(
            self.r1, json={"status": "confirmado", "restricoes": "Alergia a castanhas"}
        )
        resumo = self.dono.get(self.base + "/resumo").get_json()
        self.assertEqual(resumo["convidados"]["confirmados"], 1)
        self.assertIn(
            "Ana: Alergia a castanhas", resumo["convidados"]["restricoes_alimentares"]
        )
        for cliente in (self.dono, self.editor):
            self.assertTrue(
                any(
                    n["tipo"] == "rsvp" for n in cliente.get("/notificacoes").get_json()
                )
            )
        self.assertEqual(
            self.visitante.post(self.r1, json={"status": "talvez"}).status_code, 400
        )

    def test_rateio_servidor_centavos_fixo_e_validacao(self):
        self.assertEqual(
            self.dono.post(
                self.base + "/despesas", json={"descricao": "Bolo", "valor": 100}
            ).status_code,
            201,
        )
        self.dono.put(self.base + "/rateio", json={"ativo": True, "modo": "auto"})
        rateio = self.editor.get(self.base).get_json()["financeiro"]["rateio"]
        self.assertEqual([p["valor"] for p in rateio["pessoas"]], [33.34, 33.33, 33.33])
        self.assertEqual(rateio["pessoas"][0]["nome"], "Organizadora")
        self.assertEqual(rateio["totalArrecadado"], 100)
        fixo = self.dono.put(
            self.base + "/rateio", json={"modo": "fixo", "valorFixo": 25.5}
        ).get_json()
        self.assertEqual(fixo["totalArrecadado"], 76.5)
        for invalido in (
            {"modo": "outro"},
            {"valorFixo": "NaN"},
            {"valorFixo": -1},
            {"valorFixo": "abc"},
            {"ativo": "false"},
        ):
            self.assertEqual(
                self.dono.put(self.base + "/rateio", json=invalido).status_code, 400
            )

    def test_permissoes_sem_escalada_e_tokens(self):
        for caminho, payload in (
            ("/convidados", {"nome": "X"}),
            ("/itens-compartilhados", {"nome": "X"}),
            ("/despesas", {"descricao": "X", "valor": 10}),
            ("/locais", {}),
            ("/fotos", {}),
        ):
            self.assertEqual(
                self.leitor.post(self.base + caminho, json=payload).status_code, 403
            )
        self.assertEqual(
            self.leitor.put(self.base + "/rateio", json={"ativo": True}).status_code,
            403,
        )
        self.assertEqual(
            self.editor.post(
                self.base + "/colaboradores", json={"nome": "X", "email": "x@x.example"}
            ).status_code,
            403,
        )
        self.assertEqual(
            self.editor.put(
                self.base, json={"privacidade_convidados": "todos"}
            ).status_code,
            403,
        )
        self.assertEqual(self.visitante.get(self.base).status_code, 401)
        for r in (
            self.leitor.get(self.base).get_json(),
            self.leitor.get("/eventos").get_json()[0],
        ):
            self.assertNotIn("token_rsvp", r["lista_convidados"][0])
            self.assertNotIn("token", r["colaboradores"][0])
        self.leitor.put(
            self.base + "/colaboradores/" + self.view["id"],
            json={"status": "ativo", "pode_editar": True},
        )
        self.assertFalse(self.leitor.get(self.base).get_json()["pode_editar"])

    def test_convite_pendente_responde_pela_central(self):
        cliente = self.app.test_client()
        cliente.post(
            "/auth/cadastro",
            json={
                "nome": "Nova",
                "email": "nova@teste.example",
                "senha": "senha-teste",
            },
        )
        convite = self.dono.post(
            self.base + "/colaboradores",
            json={"nome": "Nova", "email": "nova@teste.example"},
        ).get_json()
        r = cliente.put(
            self.base + "/colaboradores/" + convite["id"], json={"status": "ativo"}
        )
        self.assertEqual(r.status_code, 200, r.get_json())
        self.assertEqual(cliente.get(self.base).status_code, 200)

    def test_saida_colaborador_libera_responsabilidade(self):
        item = self.item()
        self.editor.put(
            self.base + "/itens-compartilhados/" + item,
            json={"responsavelTipo": "usuario", "responsavelNome": "Nome forjado"},
        )
        self.assertEqual(
            self.dono.get(self.base).get_json()["itens_compartilhados"][0][
                "responsavelNome"
            ],
            "Colaborador",
        )
        self.dono.delete(self.base + "/colaboradores/" + self.colab["id"])
        self.assertFalse(
            self.dono.get(self.base).get_json()["itens_compartilhados"][0][
                "responsavelNome"
            ]
        )

    def test_lembretes_idempotentes_e_mudancas_no_convite(self):
        self.item()
        a = self.dono.get("/notificacoes").get_json()
        b = self.dono.get("/notificacoes").get_json()
        self.assertEqual(len(a), len(b))
        self.assertTrue(
            {"lembrete-presenca", "lembrete-itens"} <= {n["tipo"] for n in b}
        )
        self.dono.put(
            self.base, json={"endereco_evento": "Rua Nova, 99", "hora_evento": "19:30"}
        )
        publico = self.visitante.get(self.r1).get_json()
        self.assertEqual(publico["evento"]["local"], "Rua Nova, 99")
        self.assertTrue(any("mudaram" in n["titulo"] for n in publico["avisos"]))
        self.assertIn(
            "São+Paulo", publico["evento"]["mapas"]["google"].replace("%C3%A3", "ã")
        )
        self.assertIn("waze.com/ul?", publico["evento"]["mapas"]["waze"])

    def test_local_filtra_orcamento_capacidade_cidade_estilo(self):
        dados = {
            "nome": "Sítio Exemplo",
            "endereco": "Rua Campo, 1",
            "cidade": "São Paulo",
            "estilo": "Rústico",
            "capacidade": 50,
            "preco": 1500,
        }
        self.assertEqual(
            self.dono.post(self.base + "/locais", json=dados).status_code, 201
        )
        self.assertEqual(
            self.dono.post(self.base + "/locais", json=dados).status_code, 409
        )
        self.assertEqual(
            len(self.dono.get(self.base + "/locais").get_json()["locais"]), 1
        )
        for query in (
            "orcamento=1000",
            "capacidade=60",
            "cidade=Campinas",
            "estilo=moderno",
        ):
            self.assertEqual(
                self.dono.get(self.base + "/locais?" + query).get_json()["locais"], []
            )
        self.assertEqual(
            len(self.dono.get(self.base + "/resumo").get_json()["locais_recomendados"]),
            1,
        )
        self.assertEqual(self.leitor.delete(self.base + "/locais/1").status_code, 403)

    def test_fornecedores_contexto_avaliacoes_e_falha_externa(self):
        with patch(
            "infrastructure.provedores.google_places.GooglePlacesProvider.buscar",
            return_value=[
                {
                    "nome_empresa": "A",
                    "avaliacao": 4.2,
                    "total_avaliacoes": 10,
                    "fonte": "google",
                },
                {
                    "nome_empresa": "B",
                    "avaliacao": 4.8,
                    "total_avaliacoes": 20,
                    "fonte": "google",
                },
            ],
        ) as busca:
            r = self.dono.get(self.base + "/recomendacoes?categoria=musica").get_json()
            self.assertEqual(r["resultados"][0]["nome_empresa"], "B")
            self.assertEqual(busca.call_args.kwargs["cidade"], "São Paulo")
            self.assertIn("aniversario", busca.call_args.kwargs["termo"])
        with patch(
            "infrastructure.provedores.google_places.GooglePlacesProvider.buscar",
            side_effect=GooglePlacesIndisponivel("indisponível"),
        ):
            r = self.dono.get(self.base + "/recomendacoes?categoria=espacos")
            self.assertEqual(r.status_code, 200)
            self.assertTrue(r.get_json()["aviso"])

    def test_historico_autoria_e_acesso(self):
        item = self.item()
        self.editor.put(
            self.base + "/itens-compartilhados/" + item, json={"quantidade": 4}
        )
        logs = self.dono.get(self.base + "/logs").get_json()
        self.assertTrue(
            any(
                registro["autor"] == "Colaborador"
                and registro["acao"] == "item_compartilhado_atualizado"
                for registro in logs
            )
        )
        self.assertEqual(self.leitor.get(self.base + "/logs").status_code, 403)

    def test_fluxo_ao_vivo_e_revogacao(self):
        r = self.leitor.get(self.base + "/atualizacoes", buffered=False)
        it = iter(r.response)
        self.assertIn(b"retry:", next(it))
        self.assertIn(b"event: alteracao", next(it))
        # Usa contexto separado para simular outra sessão durante o fluxo.
        with self.app.app_context():
            c = db.session.get(ColaboradorEvento, int(self.view["id"]))
            c.status = "recusado"
            db.session.commit()
        self.assertIn(b"event: encerrado", next(it))
        r.close()
        publico = self.visitante.get(self.r1 + "/atualizacoes").data
        self.assertIn(b"event: alteracao", publico)
        self.assertNotIn(self.g1["token_rsvp"].encode(), publico)

    def test_foto_nao_expoe_chave(self):
        with self.app.app_context():
            url = self.app.extensions["momentus"].provedor.url_foto(
                "places/ABC/photos/DEF"
            )
        self.assertTrue(url.startswith("/catalogo/foto?token="))
        self.assertNotIn("key=", url)
        self.assertEqual(
            self.visitante.get("/catalogo/foto?token=invalido").status_code, 404
        )

    def test_tabelas_aditivas_preservam_dados(self):
        with self.app.app_context():
            antes = Evento.query.count()
            db.create_all()
            self.assertEqual(Evento.query.count(), antes)
            self.assertEqual(
                db.session.get(Evento, self.id).nome_evento, "Festa de teste"
            )

    def test_concorrencia_criacao_nao_duplica_produto(self):
        barreira = Barrier(2)
        cookie_sessao = self.dono.get_cookie("session").value

        def criar(nome):
            cliente = self.app.test_client()
            cliente.set_cookie("session", cookie_sessao)
            barreira.wait()
            return cliente.post(
                self.base + "/itens-compartilhados",
                json={"nome": nome, "quantidade": 2},
            ).status_code

        with ThreadPoolExecutor(max_workers=2) as executor:
            resultados = list(executor.map(criar, ["Água mineral", "agua   mineral"]))
        self.assertEqual(sorted(resultados), [201, 409])

    def test_pendencia_resolvida_sai_do_convite_e_orcamento_invalido(self):
        self.visitante.get(self.r1)
        self.visitante.post(self.r1, json={"status": "confirmado"})
        r = self.visitante.get(self.r1).get_json()
        self.assertFalse(any(a["titulo"] == "Você vai?" for a in r["avisos"]))
        for dados in ({"orcamento_evento": "NaN"}, {"rateio": {"ativo": "false"}}):
            self.assertEqual(self.dono.put(self.base, json=dados).status_code, 400)

    def test_itens_catalogo_compartilham_validacao_financeira(self):
        for dados in ({"preco": -1}, {"preco": "NaN"}, {"qtd": 0}, {"qtd": "muito"}):
            self.assertEqual(
                self.dono.post(
                    self.base + "/itens", json={"nome": "Mesa", **dados}
                ).status_code,
                400,
            )
        self.assertEqual(
            self.dono.post(
                self.base + "/itens", json={"nome": "Mesa", "preco": "12.35", "qtd": 3}
            ).status_code,
            201,
        )
        self.assertEqual(
            self.dono.get(self.base + "/resumo").get_json()["financeiro"]["total"],
            37.05,
        )


if __name__ == "__main__":
    unittest.main()
