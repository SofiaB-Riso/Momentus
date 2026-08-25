"""
Busca fornecedores reais (restaurantes, buffets, doçarias, decoração etc.)
usando a Places API (New) do Google, em vez de depender de fornecedores
cadastrados manualmente no banco.

Documentação usada como referência:
https://developers.google.com/maps/documentation/places/web-service/text-search
"""
import os

import requests

PLACES_SEARCH_URL = "https://places.googleapis.com/v1/places:searchText"

# Cada aba do catálogo vira uma consulta em texto livre para o Google.
# "todos" faz uma busca mais genérica, sem travar num tipo de serviço só.
CONSULTAS_POR_CATEGORIA = {
    "todos": "fornecedores para festas e eventos",
    "salgados": "salgados para festa",
    "doces": "doces e bolos para festa",
    "bebidas": "bebidas e bar para eventos",
    "decoracao": "decoração de festas e eventos",
    "buffet": "buffet para eventos",
}

# Campos que pedimos de volta - a Places API (New) cobra por chamada, então só
# pedimos o que a gente realmente usa no card (nome, endereço, nota, foto...).
CAMPOS_RESPOSTA = ",".join([
    "places.id",
    "places.displayName",
    "places.formattedAddress",
    "places.rating",
    "places.userRatingCount",
    "places.photos",
])


class GooglePlacesIndisponivel(Exception):
    """Erro de configuração ou de comunicação com a Places API."""


def _api_key():
    chave = os.getenv("GOOGLE_MAPS_API_KEY")
    if not chave:
        raise GooglePlacesIndisponivel(
            "Busca por fornecedores indisponível: configure GOOGLE_MAPS_API_KEY no .env."
        )
    return chave


def url_foto(nome_foto, largura=480):
    """Monta a URL pública de uma foto do Places a partir do campo 'name'
    devolvido pela busca (ex: 'places/ABC123/photos/xyz')."""
    return f"https://places.googleapis.com/v1/{nome_foto}/media?maxWidthPx={largura}&key={_api_key()}"


def buscar_fornecedores_perto(categoria, lat=None, lng=None, cidade=None, termo=None, raio_metros=8000):
    """Retorna uma lista de fornecedores (dicts) vindos do Google Places.

    Pelo menos um entre (lat + lng) ou cidade deve ser informado, senão o
    Google não tem como saber "perto de onde" buscar.
    """
    # Quando o usuário digita um termo na busca do catálogo, ele quer achar
    # aquele estabelecimento pelo nome — então o termo vira a consulta em si,
    # em vez de ficar misturado com o texto genérico da categoria.
    if termo:
        consulta = termo
    else:
        consulta = CONSULTAS_POR_CATEGORIA.get(categoria, CONSULTAS_POR_CATEGORIA["todos"])

    corpo = {"textQuery": consulta, "languageCode": "pt-BR", "maxResultCount": 12}

    if lat is not None and lng is not None:
        corpo["locationBias"] = {
            "circle": {"center": {"latitude": lat, "longitude": lng}, "radius": raio_metros}
        }
    elif cidade:
        corpo["textQuery"] = f"{consulta} em {cidade}"
    else:
        raise GooglePlacesIndisponivel("Informe lat/lng ou uma cidade para buscar fornecedores perto de você.")

    try:
        resposta = requests.post(
            PLACES_SEARCH_URL,
            json=corpo,
            headers={
                "Content-Type": "application/json",
                "X-Goog-Api-Key": _api_key(),
                "X-Goog-FieldMask": CAMPOS_RESPOSTA,
            },
            timeout=8,
        )
        resposta.raise_for_status()
    except requests.RequestException as erro:
        raise GooglePlacesIndisponivel(f"Não foi possível falar com o Google agora: {erro}") from erro

    dados = resposta.json()
    resultado = []
    for lugar in dados.get("places", []):
        fotos = lugar.get("photos") or []
        resultado.append({
            "id": lugar.get("id"),
            "nome_empresa": (lugar.get("displayName") or {}).get("text", "Fornecedor"),
            "endereco": lugar.get("formattedAddress", ""),
            "avaliacao": lugar.get("rating"),
            "total_avaliacoes": lugar.get("userRatingCount", 0),
            "categoria": categoria,
            "foto_url": url_foto(fotos[0]["name"]) if fotos else None,
            "fonte": "google",
        })
    return resultado
