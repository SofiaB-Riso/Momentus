from datetime import timedelta
from hashlib import sha256
from secrets import token_urlsafe

from application.erros import DadosInvalidos
from models.tempo import utcnow

from services.caso_uso import CasoUso


class GerarLinkResponsavelService(CasoUso):
    def executar(self):
        registro = self.usuario_atual(exigir_autorizacao=False).autorizacao_conta
        if (
            not registro
            or registro.faixa_etaria != "menor"
            or registro.status == "autorizado"
        ):
            raise DadosInvalidos(
                "O link é destinado a contas aguardando autorização de responsável."
            )
        token = token_urlsafe(32)
        registro.token_hash = sha256(token.encode()).hexdigest()
        registro.expira_em = utcnow() + timedelta(days=7)
        registro.status = "pendente"
        self.transacao.confirmar()
        return {
            "link": "/autorizacao.html#tipo=conta&token=" + token,
            "validade_dias": 7,
        }
