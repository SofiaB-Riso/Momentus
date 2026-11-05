"""Caso de integração: consultar uma página de estabelecimentos no Google Places."""

import math
from urllib.parse import urlencode

import requests
from application.erros import IntegracaoIndisponivel

from services.integracoes.google_base_service import GoogleBaseService

GooglePlacesIndisponivel = IntegracaoIndisponivel

PLACES_SEARCH_URL = "https://places.googleapis.com/v1/places:searchText"
CONSULTAS_POR_CATEGORIA = {
    "todos": "fornecedores para festas e eventos",
    "salgados": "salgados para festa",
    "doces": "doces e bolos para festa",
    "bebidas": "bebidas e bar para eventos",
    "decoracao": "decoração de festas e eventos",
    "buffet": "buffet para eventos",
    "musica": "DJ bandas e música para eventos",
    "espacos": "espaços salões e sítios para alugar para festas",
}
CAMPOS_RESPOSTA = ",".join(
    [
        "nextPageToken",
        "places.id",
        "places.displayName",
        "places.formattedAddress",
        "places.rating",
        "places.userRatingCount",
        "places.location",
    ]
)


class BuscarLugaresGoogleService(GoogleBaseService):
    def executar(
        self,
        categoria,
        lat=None,
        lng=None,
        cidade=None,
        termo=None,
        raio_metros=5000,
        pagina=None,
        avaliacao_minima=None,
    ):
        """Uma página do Google, sem carregar páginas extras automaticamente."""
        if termo:
            consulta = termo
        else:
            consulta = CONSULTAS_POR_CATEGORIA.get(
                categoria, CONSULTAS_POR_CATEGORIA["todos"]
            )
        corpo = {"textQuery": consulta, "languageCode": "pt-BR", "pageSize": 20}
        if pagina:
            corpo["pageToken"] = pagina
        if avaliacao_minima is not None:
            corpo["minRating"] = avaliacao_minima
        origem = (lat, lng) if lat is not None and lng is not None else None
        if origem:
            corpo["rankPreference"] = "DISTANCE"
            corpo["locationBias"] = {
                "circle": {
                    "center": {"latitude": lat, "longitude": lng},
                    "radius": raio_metros,
                }
            }
        elif cidade:
            corpo["textQuery"] = f"{consulta} em {cidade}"
        else:
            raise GooglePlacesIndisponivel(
                "Informe lat/lng ou uma cidade para buscar fornecedores perto de você."
            )
        try:
            resposta = self.http.post(
                PLACES_SEARCH_URL,
                json=corpo,
                headers={
                    "Content-Type": "application/json",
                    "X-Goog-Api-Key": self._api_key(),
                    "X-Goog-FieldMask": CAMPOS_RESPOSTA,
                },
                timeout=8,
            )
            resposta.raise_for_status()
        except requests.RequestException as erro:
            raise GooglePlacesIndisponivel(
                "Não foi possível consultar fornecedores agora. Tente novamente mais tarde."
            ) from erro
        try:
            dados = resposta.json()
        except ValueError as erro:
            raise GooglePlacesIndisponivel(
                "Resposta inválida do serviço de busca."
            ) from erro
        if not isinstance(dados, dict) or not isinstance(dados.get("places", []), list):
            raise GooglePlacesIndisponivel("Resposta inválida do serviço de busca.")
        resultado = []
        for lugar in dados.get("places", []):
            localizacao = lugar.get("location") or {}
            lat_local = localizacao.get("latitude")
            lng_local = localizacao.get("longitude")
            street_view = None
            distancia = None
            if (
                type(lat_local) in (float, int)
                and type(lng_local) in (float, int)
                and -90 <= lat_local <= 90
                and -180 <= lng_local <= 180
            ):
                if origem:
                    delta_lat = math.radians(lat_local - origem[0])
                    delta_lng = math.radians(lng_local - origem[1])
                    arco = (
                        math.sin(delta_lat / 2) ** 2
                        + math.cos(math.radians(origem[0]))
                        * math.cos(math.radians(lat_local))
                        * math.sin(delta_lng / 2) ** 2
                    )
                    distancia = 6371000 * 2 * math.asin(math.sqrt(min(1, arco)))
                street_view = "https://www.google.com/maps/@?" + urlencode(
                    {
                        "api": 1,
                        "map_action": "pano",
                        "viewpoint": f"{lat_local},{lng_local}",
                    }
                )
            resultado.append(
                {
                    "id": lugar.get("id"),
                    "nome_empresa": (lugar.get("displayName") or {}).get(
                        "text", "Fornecedor"
                    ),
                    "endereco": lugar.get("formattedAddress", ""),
                    "avaliacao": lugar.get("rating"),
                    "total_avaliacoes": lugar.get("userRatingCount", 0),
                    "categoria": categoria,
                    "google_maps_url": "https://www.google.com/maps/search/?"
                    + urlencode(
                        {
                            "api": 1,
                            "query": lugar.get("formattedAddress", ""),
                            "query_place_id": lugar.get("id", ""),
                        }
                    ),
                    "street_view_url": street_view,
                    "distancia_metros": round(distancia, 1)
                    if distancia is not None
                    else None,
                    "fonte": "google",
                }
            )
        if origem:
            # Distâncias desconhecidas ficam no final, sem excluir estabelecimentos.
            resultado.sort(
                key=lambda lugar: (
                    lugar["distancia_metros"] is None,
                    lugar["distancia_metros"] or 0,
                )
            )
        proxima = dados.get("nextPageToken")
        return {
            "fornecedores": resultado,
            "proxima_pagina": proxima if isinstance(proxima, str) and proxima else None,
        }
