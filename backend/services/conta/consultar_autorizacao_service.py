from services.caso_uso import CasoUso


class ConsultarAutorizacaoContaService(CasoUso):
    def executar(self):
        registro = self.usuario_atual(exigir_autorizacao=False).autorizacao_conta
        return registro.to_dict() if registro else {"status": "nao_informado"}
