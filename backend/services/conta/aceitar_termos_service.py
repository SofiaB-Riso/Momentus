from application.erros import DadosInvalidos
from models import PrivacidadeUsuario
from models.tempo import utcnow
from utils.validacao import validar_entrada

from services.caso_uso import CasoUso
from services.conta.termos import VERSAO_TERMOS


class AceitarTermosService(CasoUso):
    def executar(self, dados, confirmar=True):
        dados = validar_entrada(dados)
        if dados.get("aceite_termos") is not True:
            raise DadosInvalidos("Leia e aceite os Termos de Uso para continuar.")
        if dados.get("versao_termos") != VERSAO_TERMOS:
            raise DadosInvalidos(
                "Os termos foram atualizados. Reabra a página e leia a versão atual."
            )
        registro = PrivacidadeUsuario.buscar_por_id(self.usuario_id)
        if registro is None:
            registro = PrivacidadeUsuario(usuario_id=self.usuario_id).salvar(
                confirmar=False
            )
        # Aceitar de novo a mesma versão não muda a data original do registro.
        if registro.termos_versao != VERSAO_TERMOS:
            registro.termos_versao = VERSAO_TERMOS
            registro.aceito_em = utcnow()
        if confirmar:
            self.transacao.confirmar()
        return registro.to_dict()
