"""Adapta os contratos de fornecedores aos Services de integração do Google.

As requisições HTTP são executadas exclusivamente nos Services; este adaptador
mantém os contratos usados pelos casos de uso e pelos testes existentes.
"""

from application.erros import IntegracaoIndisponivel as GooglePlacesIndisponivel
from services.integracoes.buscar_foto_google_service import BuscarFotoGoogleService
from services.integracoes.buscar_lugares_google_service import (
    BuscarLugaresGoogleService,
)


class GooglePlacesProvider:
    def __init__(self, api_key, secret_key, http=None):
        self.busca = BuscarLugaresGoogleService(api_key, http)
        self.fotos = BuscarFotoGoogleService(api_key, secret_key, http)

    def buscar(self, categoria, **filtros):
        return self.buscar_pagina(categoria, **filtros)["fornecedores"]

    def buscar_pagina(self, categoria, **filtros):
        return self.busca.executar(categoria, **filtros)

    def foto(self, token):
        return self.fotos.executar(token)

    def url_foto(self, nome_foto, largura=480):
        return self.fotos.url_foto(nome_foto, largura)


__all__ = ["GooglePlacesProvider", "GooglePlacesIndisponivel"]
