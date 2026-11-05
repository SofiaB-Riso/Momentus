import requests
from application.erros import IntegracaoIndisponivel


class GoogleBaseService:
    def __init__(self, api_key, http=None):
        self.api_key = api_key
        self.http = http if http is not None else requests.Session()

    def _api_key(self):
        if not self.api_key:
            raise IntegracaoIndisponivel(
                "Busca por fornecedores indisponível: configure GOOGLE_MAPS_API_KEY no .env."
            )
        return self.api_key
