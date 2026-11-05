from application.erros import NaoEncontrado
from repositories.autorizacao_repository import AutorizacaoRepository
from utils.validacao import validar_entrada

from services.caso_uso import CasoUso
from services.conta.termos import VERSAO_TERMOS


class VerLinkResponsavelService(CasoUso):
    def executar(self, dados):
        dados = validar_entrada(dados)
        registro, titular = AutorizacaoRepository.pelo_token(
            dados.get("tipo"), dados.get("token")
        )
        if not titular:
            raise NaoEncontrado(
                "Link inválido, utilizado ou expirado. Solicite outro link."
            )
        return {
            "nome": titular.nome,
            "tipo": dados["tipo"],
            "versao": VERSAO_TERMOS,
            "evento": titular.evento.nome_evento
            if dados["tipo"] == "convidado"
            else None,
        }
