import math
import re
from urllib.parse import urlencode

import requests
from application.erros import IntegracaoIndisponivel, NaoEncontrado
from itsdangerous import BadSignature, URLSafeTimedSerializer

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


class GooglePlacesProvider:
    def __init__(self, api_key, secret_key, http=None):
        self.api_key = api_key
        self.secret_key = secret_key
        self.http = http if http is not None else requests.Session()

    def _api_key(self):
        if not self.api_key:
            raise GooglePlacesIndisponivel(
                "Busca por fornecedores indisponível: configure GOOGLE_MAPS_API_KEY no .env."
            )
        return self.api_key

    def foto(self, token):
        try:
            nome = URLSafeTimedSerializer(self.secret_key, salt="foto-places").loads(
                token, max_age=3600
            )
            if not isinstance(nome, str) or not re.fullmatch(
                r"places/[\w-]+/photos/[\w-]+", nome
            ):
                raise BadSignature("Foto inválida")
        except BadSignature:
            raise NaoEncontrado("Foto indisponível.") from None
        try:
            resposta = self.http.get(
                f"https://places.googleapis.com/v1/{nome}/media",
                params={"maxWidthPx": 480, "key": self._api_key()},
                timeout=8,
            )
            resposta.raise_for_status()
            tipo = resposta.headers.get("Content-Type", "")
            if not tipo.startswith("image/"):
                raise GooglePlacesIndisponivel("Foto indisponível.")
            return resposta.content, tipo
        except requests.RequestException:
            raise GooglePlacesIndisponivel("Foto indisponível.") from None

    def url_foto(self, nome_foto, largura=480):
        """Monta a URL pública de uma foto do Places a partir do campo 'name'
        devolvido pela busca (ex: 'places/ABC123/photos/xyz')."""
        token = URLSafeTimedSerializer(self.secret_key, salt="foto-places").dumps(
            nome_foto
        )
        return "/catalogo/foto?" + urlencode({"token": token})

    def buscar(
        self, categoria, lat=None, lng=None, cidade=None, termo=None, raio_metros=5000
    ):
        """Compatibilidade com o Início e as recomendações, que recebem uma lista."""
        return self.buscar_pagina(
            categoria,
            lat=lat,
            lng=lng,
            cidade=cidade,
            termo=termo,
            raio_metros=raio_metros,
        )["fornecedores"]

    def buscar_pagina(
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
