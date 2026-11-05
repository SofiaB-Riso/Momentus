from application.erros import Proibido


class VerificarAutorizacaoContaService:
    def executar(self, usuario):
        registro = usuario.autorizacao_conta if usuario else None
        if not registro or registro.status != "autorizado":
            raise Proibido(
                "Conclua a declaração de idade e, quando necessário, a autorização do responsável em Configurações.",
                codigo="AUTHORIZATION_REQUIRED",
            )
