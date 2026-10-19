"""Proximidade, busca sem fotos, Street View e proxy legado; Google simulado."""

import json
import math
import unittest
from unittest.mock import Mock
from urllib.parse import parse_qs, urlparse

from application.erros import DadosInvalidos, IntegracaoIndisponivel, NaoEncontrado
from infrastructure.provedores.google_places import GooglePlacesProvider
from services.catalogo_service import FornecedoresPertoService


class CatalogoGoogleTest(unittest.TestCase):
    def setUp(self):
        self.http = Mock()
        self.provedor = GooglePlacesProvider(
            "chave-simulada", "segredo-teste", self.http
        )

    def test_busca_sem_fotos_mantem_street_view_sem_chave(self):
        self.http.post.return_value.json.return_value = {
            "places": [
                {
                    "id": "ABC",
                    "displayName": {"text": "Buffet de teste"},
                    "formattedAddress": "Rua 1",
                    "location": {"latitude": 0, "longitude": -46.5},
                    "googleMapsUri": "https://maps.google.com/?cid=1",
                    "photos": [
                        {
                            "name": "places/ABC/photos/FOTO1",
                            "googleMapsUri": "https://maps.google.com/foto1",
                            "authorAttributions": [
                                {
                                    "displayName": "Autora",
                                    "uri": "https://maps.google.com/autora",
                                    "photoUri": "https://example.com/avatar.png",
                                }
                            ],
                        },
                        {"name": "places/ABC/photos/FOTO2"},
                        {},
                    ],
                }
            ]
        }
        resultado = self.provedor.buscar("buffet", cidade="São Paulo")[0]
        self.assertNotIn("fotos", resultado)
        self.assertNotIn("foto_url", resultado)
        self.assertNotIn("foto_autores", resultado)
        self.http.get.assert_not_called()
        query = parse_qs(urlparse(resultado["street_view_url"]).query)
        self.assertEqual(query["map_action"], ["pano"])
        self.assertEqual(query["viewpoint"], ["0,-46.5"])
        self.assertNotIn("chave-simulada", json.dumps(resultado))
        self.assertNotIn(
            "places.photos",
            self.http.post.call_args.kwargs["headers"]["X-Goog-FieldMask"],
        )

    def test_busca_sem_fotos_ou_coordenadas_nao_inventa_imagem(self):
        self.http.post.return_value.json.return_value = {
            "places": [
                {
                    "id": "ABC",
                    "displayName": {"text": "Sem fotos"},
                    "photos": [{}, {"name": "https://invalido.example/foto"}],
                }
            ]
        }
        resultado = self.provedor.buscar("buffet", cidade="São Paulo")[0]
        self.assertNotIn("foto_url", resultado)
        self.assertNotIn("fotos", resultado)
        self.assertIsNone(resultado["street_view_url"])
        self.assertEqual(
            parse_qs(urlparse(resultado["google_maps_url"]).query)["query_place_id"],
            ["ABC"],
        )

    def test_proxy_entrega_imagem_e_rejeita_token_ou_conteudo_invalido(self):
        foto = self.http.get.return_value
        foto.headers = {"Content-Type": "image/jpeg"}
        foto.content = b"imagem-simulada"
        token = parse_qs(
            urlparse(self.provedor.url_foto("places/ABC/photos/FOTO1")).query
        )["token"][0]
        self.assertEqual(self.provedor.foto(token), (b"imagem-simulada", "image/jpeg"))
        self.assertIn("places/ABC/photos/FOTO1/media", self.http.get.call_args.args[0])
        with self.assertRaises(NaoEncontrado):
            self.provedor.foto("adulterado")
        foto.headers = {"Content-Type": "application/json"}
        with self.assertRaises(IntegracaoIndisponivel):
            self.provedor.foto(token)

    def lugares(self, *locais):
        self.http.post.return_value.json.return_value = {
            "places": [
                {
                    "id": nome,
                    "displayName": {"text": nome},
                    "location": {"latitude": lat, "longitude": lng},
                }
                for nome, lat, lng in locais
            ]
        }

    def test_coordenadas_ordenam_por_distancia_sem_excluir_longe(self):
        self.lugares(
            ("longe", -19.9, -43.94),
            ("medio", -19.82, -43.94),
            ("perto", -19.805, -43.94),
        )
        dados = self.provedor.buscar("todos", lat=-19.8, lng=-43.94)
        self.assertEqual([d["id"] for d in dados], ["perto", "medio", "longe"])
        self.assertAlmostEqual(dados[0]["distancia_metros"], 556, delta=1)
        self.assertAlmostEqual(dados[1]["distancia_metros"], 2224, delta=1)
        corpo = self.http.post.call_args.kwargs["json"]
        self.assertEqual(corpo["rankPreference"], "DISTANCE")
        self.assertEqual(
            corpo["locationBias"]["circle"]["center"],
            {"latitude": -19.8, "longitude": -43.94},
        )
        self.assertEqual(corpo["locationBias"]["circle"]["radius"], 5000)

    def test_busca_proxima_mantem_local_sem_coordenadas_no_final(self):
        self.lugares(
            ("ausente", None, None),
            ("nan", float("nan"), 0),
            ("bool", False, 0),
            ("fora", 91, 0),
            ("string", "0", "0"),
            ("valido", 0, 0),
        )
        dados = self.provedor.buscar("todos", lat=0, lng=0)
        self.assertEqual(dados[0]["id"], "valido")
        self.assertEqual(len(dados), 6)
        self.assertEqual(dados[0]["distancia_metros"], 0)
        self.assertTrue(all(d["distancia_metros"] is None for d in dados[1:]))

    def test_busca_por_bairro_e_cidade_nao_inventa_distancia(self):
        self.lugares(("local", None, None))
        dados = self.provedor.buscar("buffet", cidade="Guarani, Belo Horizonte")
        corpo = self.http.post.call_args.kwargs["json"]
        self.assertIn("em Guarani, Belo Horizonte", corpo["textQuery"])
        self.assertNotIn("locationBias", corpo)
        self.assertNotIn("rankPreference", corpo)
        self.assertEqual(len(dados), 1)
        self.assertIsNone(dados[0]["distancia_metros"])

    def test_busca_inclui_resultados_alem_do_raio_de_preferencia(self):
        self.lugares(
            ("dentro", math.degrees(4999 / 6371000), 0),
            ("fora", math.degrees(75000 / 6371000), 0),
        )
        dados = self.provedor.buscar("todos", lat=0, lng=0)
        self.assertEqual([d["id"] for d in dados], ["dentro", "fora"])

    def test_distancia_funciona_ao_cruzar_antimeridiano(self):
        self.lugares(("perto", 0, -179.999), ("longe", 0, -179))
        dados = self.provedor.buscar("todos", lat=0, lng=179.999)
        self.assertEqual([d["id"] for d in dados], ["perto", "longe"])
        self.assertAlmostEqual(dados[0]["distancia_metros"], 222.4, delta=1)

    def test_servico_rejeita_coordenadas_invalidas_ou_incompletas(self):
        provedor = Mock()
        servico = FornecedoresPertoService(None, None, provedor)
        for params in [
            {"lat": "0", "cidade": "BH"},
            {"lng": "0", "cidade": "BH"},
            {"lat": "nan", "lng": "0"},
            {"lat": "91", "lng": "0"},
            {"lat": "0", "lng": "inf"},
            {"lat": "abc", "lng": "0"},
        ]:
            with self.subTest(params=params), self.assertRaises(DadosInvalidos):
                servico.executar(params)
        provedor.buscar.assert_not_called()

    def test_servico_preserva_coordenadas_zero(self):
        provedor = Mock()
        servico = FornecedoresPertoService(None, None, provedor)
        servico.executar({"lat": "0", "lng": "0"})
        provedor.buscar.assert_called_once_with(
            "todos", lat=0.0, lng=0.0, cidade=None, termo=None
        )
