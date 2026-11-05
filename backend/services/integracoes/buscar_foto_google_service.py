"""Caso de integração legado: validar um token e consultar uma foto do Google."""

import re
from urllib.parse import urlencode

import requests
from application.erros import IntegracaoIndisponivel, NaoEncontrado
from itsdangerous import BadSignature, URLSafeTimedSerializer

from services.integracoes.google_base_service import GoogleBaseService

GooglePlacesIndisponivel = IntegracaoIndisponivel


class BuscarFotoGoogleService(GoogleBaseService):
    def __init__(self, api_key, secret_key, http=None):
        super().__init__(api_key, http)
        self.secret_key = secret_key

    def executar(self, token):
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
