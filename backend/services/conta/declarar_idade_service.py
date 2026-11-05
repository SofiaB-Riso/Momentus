from application.erros import Conflito, DadosInvalidos
from models import AutorizacaoConta
from models.tempo import utcnow
from utils.validacao import validar_entrada

from services.caso_uso import CasoUso
from services.conta.termos import VERSAO_TERMOS


class DeclararIdadeService(CasoUso):
    def executar(self, dados, confirmar=True):
        dados = validar_entrada(dados)
        faixa = dados.get("faixa_etaria")
        if (
            faixa not in {"adulto", "menor"}
            or dados.get("declaracao_idade") is not True
        ):
            raise DadosInvalidos(
                "Declare se tem 18 anos ou mais ou se precisa de autorização de responsável."
            )
        registro = AutorizacaoConta.buscar_por_id(self.usuario_id)
        if registro:
            if registro.faixa_etaria != faixa:
                raise Conflito(
                    "Para corrigir a declaração de idade, use o canal de privacidade."
                )
            return registro.to_dict()
        registro = AutorizacaoConta(
            usuario_id=self.usuario_id,
            faixa_etaria=faixa,
            status="autorizado" if faixa == "adulto" else "pendente",
            versao=VERSAO_TERMOS,
            autorizado_em=utcnow() if faixa == "adulto" else None,
        ).salvar(confirmar=False)
        if confirmar:
            self.transacao.confirmar()
        return registro.to_dict()
