from models import PrivacidadeUsuario

from services.caso_uso import CasoUso
from services.conta.termos import VERSAO_TERMOS


class ConsultarPrivacidadeService(CasoUso):
    def __init__(self, transacao, usuario_id, config):
        super().__init__(transacao, usuario_id)
        self.config = config

    def executar(self):
        registro = (
            PrivacidadeUsuario.buscar_por_id(self.usuario_id)
            if self.usuario_id
            else None
        )
        return {
            "versao": VERSAO_TERMOS,
            "aceite": registro.to_dict() if registro else None,
            "responsavel": self.config.get("PRIVACY_CONTROLLER", ""),
            "encarregado": self.config.get("PRIVACY_OFFICER", ""),
            "email": self.config.get("PRIVACY_EMAIL", ""),
            "telefone": self.config.get("PRIVACY_PHONE", ""),
            "demonstracao": self.config.get("PRIVACY_DEMO", True),
        }
