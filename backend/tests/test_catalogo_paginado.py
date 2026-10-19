"""Paginação e seleção de avaliações com Google simulado."""

import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock

os.environ["DATABASE_URL"] = "sqlite://"
from app import create_app
from application.erros import DadosInvalidos, IntegracaoIndisponivel
from infrastructure.provedores.google_places import GooglePlacesProvider
from models import db
from services.catalogo_service import CatalogoPaginadoService


def item(identificador, nota=4.5, quantidade=201, distancia=100):
    return dict(
        id=identificador,
        nome_empresa=identificador,
        avaliacao=nota,
        total_avaliacoes=quantidade,
        distancia_metros=distancia,
    )


class CatalogoPaginadoTest(unittest.TestCase):
    def setUp(self):
        self.http = Mock()
        self.google = GooglePlacesProvider("chave-simulada", "segredo", self.http)
        self.provedor = Mock()
        self.servico = CatalogoPaginadoService(None, None, self.provedor)

    def test_pede_cursor_e_nao_carrega_paginas_automaticamente(self):
        self.http.post.return_value.json.return_value = {
            "places": [],
            "nextPageToken": "dois",
        }
        self.assertEqual(
            self.google.buscar_pagina("buffet", cidade="BH"),
            {"fornecedores": [], "proxima_pagina": "dois"},
        )
        chamada = self.http.post.call_args.kwargs
        self.assertIn(
            "nextPageToken", chamada["headers"]["X-Goog-FieldMask"].split(",")
        )
        self.assertNotIn("pageToken", chamada["json"])
        self.assertEqual(self.http.post.call_count, 1)

    def test_parametros_sao_identicos_entre_paginas(self):
        self.http.post.return_value.json.return_value = {
            "places": [],
            "nextPageToken": "dois",
        }
        filtros = dict(lat=-19.8, lng=-43.9, termo="buffet", avaliacao_minima=4.0)
        self.google.buscar_pagina("todos", **filtros)
        inicial = self.http.post.call_args.kwargs["json"].copy()
        self.google.buscar_pagina("todos", pagina="dois", **filtros)
        segunda = self.http.post.call_args.kwargs["json"].copy()
        self.assertEqual(segunda.pop("pageToken"), "dois")
        self.assertEqual(inicial, segunda)
        self.assertEqual(inicial["minRating"], 4.0)

    def test_pagina_final_e_lista_legada(self):
        self.http.post.return_value.json.return_value = {"places": [{"id": "um"}]}
        pagina = self.google.buscar_pagina("buffet", cidade="BH")
        self.assertIsNone(pagina["proxima_pagina"])
        self.assertEqual(
            self.google.buscar("buffet", cidade="BH"), pagina["fornecedores"]
        )

    def test_resposta_invalida_controlada(self):
        for resposta in [[], {"places": "invalido"}]:
            with self.subTest(resposta=resposta):
                self.http.post.return_value.json.return_value = resposta
                with self.assertRaises(IntegracaoIndisponivel):
                    self.google.buscar_pagina("buffet", cidade="BH")

    def test_ambos_os_limites_sao_estritos(self):
        self.provedor.buscar_pagina.return_value = {
            "fornecedores": [
                item("nota-exata", 4, 1000),
                item("quantidade-exata", 5, 200),
                item("valido", 4.1, 201),
                item("poucas", 4.9, 199),
                item("sem-nota", None, 900),
                item("sem-quantidade", 5, None),
            ],
            "proxima_pagina": "dois",
        }
        dados = self.servico.executar({"categoria": "melhores", "cidade": "BH"})
        self.assertEqual([f["id"] for f in dados["fornecedores"]], ["valido"])
        self.assertEqual(dados["proxima_pagina"], "dois")
        self.provedor.buscar_pagina.assert_called_once_with(
            categoria="todos",
            cidade="BH",
            lat=None,
            lng=None,
            termo=None,
            avaliacao_minima=4.0,
            pagina=None,
        )

    def test_ordena_por_nota_contagem_e_distancia(self):
        self.provedor.buscar_pagina.return_value = {
            "fornecedores": [
                item("perto", 4.8, 500, 10),
                item("nota", 5, 201, 900),
                item("contagem", 4.8, 1000, 500),
                item("longe", 4.8, 500, 1000),
                item("sem-distancia", 4.8, 500, None),
            ],
            "proxima_pagina": None,
        }
        dados = self.servico.executar({"categoria": "melhores", "cidade": "BH"})
        self.assertEqual(
            [f["id"] for f in dados["fornecedores"]],
            ["nota", "contagem", "perto", "longe", "sem-distancia"],
        )

    def test_categoria_normal_sem_restricao_de_avaliacao(self):
        itens = [item("poucas", 3.9, 20)]
        self.provedor.buscar_pagina.return_value = {
            "fornecedores": itens,
            "proxima_pagina": None,
        }
        dados = self.servico.executar(
            {"categoria": "doces", "cidade": "BH", "pagina": "dois"}
        )
        self.assertEqual(dados["fornecedores"], itens)
        self.assertNotIn(
            "avaliacao_minima", self.provedor.buscar_pagina.call_args.kwargs
        )
        self.assertEqual(self.provedor.buscar_pagina.call_args.kwargs["pagina"], "dois")

    def test_pagina_sem_qualificados_ainda_permite_carregar_mais(self):
        self.provedor.buscar_pagina.return_value = {
            "fornecedores": [item("baixa", 3, 900)],
            "proxima_pagina": "outra",
        }
        self.assertEqual(
            self.servico.executar({"categoria": "melhores", "cidade": "BH"}),
            {"fornecedores": [], "proxima_pagina": "outra"},
        )
        self.assertEqual(self.provedor.buscar_pagina.call_count, 1)

    def test_valida_antes_de_consultar(self):
        for params in [
            {},
            {"cidade": "BH", "pagina": "x" * 8193},
            {"cidade": "BH", "lat": "abc", "lng": "0"},
        ]:
            with (
                self.subTest(params=str(params)[:80]),
                self.assertRaises(DadosInvalidos),
            ):
                self.servico.executar(params)
        self.provedor.buscar_pagina.assert_not_called()


class CatalogoPaginadoHTTPTest(unittest.TestCase):
    def setUp(self):
        self.pasta = tempfile.TemporaryDirectory(prefix="momentus-paginacao-")
        self.app = create_app(
            {
                "TESTING": True,
                "SECRET_KEY": "teste",
                "SQLALCHEMY_DATABASE_URI": "sqlite:///"
                + str(Path(self.pasta.name) / "teste.db"),
                "UPLOAD_FOLDER": self.pasta.name,
            }
        )
        self.cliente = self.app.test_client()
        self.provedor = Mock()
        self.app.extensions["momentus"].provedor = self.provedor

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.engine.dispose()
        self.pasta.cleanup()

    def test_endpoint_preserva_lista_do_inicio(self):
        self.provedor.buscar.return_value = [item("legado")]
        resposta = self.cliente.get("/catalogo/perto?cidade=BH")
        self.assertEqual(resposta.status_code, 200)
        self.assertIsInstance(resposta.json, list)
        self.provedor.buscar_pagina.return_value = {
            "fornecedores": [item("novo")],
            "proxima_pagina": "dois",
        }
        resposta = self.cliente.get(
            "/catalogo/perto?paginado=1&categoria=melhores&cidade=BH"
        )
        self.assertEqual(resposta.status_code, 200)
        self.assertEqual(resposta.json["proxima_pagina"], "dois")
        self.assertEqual(resposta.json["fornecedores"][0]["id"], "novo")

    def test_falha_externa_retorna_502(self):
        self.provedor.buscar_pagina.side_effect = IntegracaoIndisponivel(
            "Tente novamente."
        )
        resposta = self.cliente.get(
            "/catalogo/perto?paginado=1&categoria=melhores&cidade=BH&pagina=dois"
        )
        self.assertEqual(resposta.status_code, 502)
        self.assertEqual(resposta.json["erro"], "Tente novamente.")
