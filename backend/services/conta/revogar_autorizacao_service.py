from application.erros import DadosInvalidos
from models.tempo import utcnow

from services.caso_uso import CasoUso


class RevogarAutorizacaoContaService(CasoUso):
    def executar(self):
        registro = self.usuario_atual(exigir_autorizacao=False).autorizacao_conta
        if not registro or registro.faixa_etaria != "menor":
            raise DadosInvalidos(
                "Não há autorização de responsável para revogar nesta conta."
            )
        registro.status = "revogado"
        registro.revogado_em = utcnow()
        registro.token_hash = None
        registro.expira_em = None
        self.transacao.confirmar()
        return registro.to_dict()
