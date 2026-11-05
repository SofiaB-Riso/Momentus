from application.erros import DadosInvalidos, NaoEncontrado
from models.tempo import utcnow
from repositories.autorizacao_repository import AutorizacaoRepository
from repositories.consulta_evento_repository import ConsultaEventoRepository
from utils.validacao import normalizar_email, validar_entrada, validar_nome

from services.caso_uso import CasoUso
from services.conta.termos import VERSAO_TERMOS
from services.convidados.informacoes_alimentares_service import (
    RegistrarInformacoesAlimentaresService,
)
from services.lista_espera.organizar_fila_service import OrganizarFilaService


class ResponderAutorizacaoResponsavelService(CasoUso):
    def executar(self, dados):
        dados = validar_entrada(dados)
        registro, titular = AutorizacaoRepository.pelo_token(
            dados.get("tipo"), dados.get("token")
        )
        if not titular:
            raise NaoEncontrado("Link inválido, utilizado ou expirado.")
        if (
            dados.get("declaracao_responsavel") is not True
            or dados.get("versao_consentimento") != VERSAO_TERMOS
        ):
            raise DadosInvalidos(
                "O responsável deve ler os documentos e confirmar sua declaração."
            )
        nome = validar_nome(dados.get("responsavel_nome"))
        email = normalizar_email(dados.get("responsavel_email"))
        vinculo = dados.get("vinculo")
        if not isinstance(vinculo, str) or not 2 <= len(vinculo.strip()) <= 100:
            raise DadosInvalidos("Informe seu vínculo com o titular.")
        if dados["tipo"] == "conta" and type(dados.get("autorizar_conta")) is not bool:
            raise DadosInvalidos("Escolha se autoriza o uso da conta.")
        if (
            dados["tipo"] == "convidado"
            and type(dados.get("autorizar_saude")) is not bool
        ):
            raise DadosInvalidos("Escolha se autoriza as informações de saúde.")
        if (
            dados["tipo"] == "convidado"
            and type(dados.get("autorizar_participacao")) is not bool
        ):
            raise DadosInvalidos(
                "Escolha se autoriza o uso dos dados para a participação no evento."
            )
        if dados["tipo"] == "convidado":
            ConsultaEventoRepository.bloquear(titular.evento_id)
        if not AutorizacaoRepository.consumir(registro):
            raise DadosInvalidos("Este link já foi utilizado. Solicite outro.")
        if dados["tipo"] == "conta":
            registro.status = "autorizado" if dados["autorizar_conta"] else "negado"
            registro.autorizado_em = utcnow() if dados["autorizar_conta"] else None
            registro.revogado_em = None
            registro.versao = VERSAO_TERMOS
            registro.responsavel_nome, registro.responsavel_email, registro.vinculo = (
                nome,
                email,
                vinculo.strip(),
            )
        else:
            registro.versao = VERSAO_TERMOS
            registro.origem = "responsavel"
            registro.responsavel_nome, registro.responsavel_email, registro.vinculo = (
                nome,
                email,
                vinculo.strip(),
            )
            registro.responsavel_autorizou = dados["autorizar_participacao"]
            registro.responsavel_autorizado_em = utcnow()
            if not dados["autorizar_participacao"]:
                titular.status = "recusado"
                OrganizarFilaService().cancelar(titular)
                OrganizarFilaService().promover(titular.evento)
                titular.restricoes_alimentares = ""
                dados = {**dados, "saude": "", "autorizar_saude": False}
                from services.itens.liberacao_service import (
                    LiberarItensConvidadoService,
                )

                LiberarItensConvidadoService().executar(titular)
            RegistrarInformacoesAlimentaresService().executar(
                titular, dados, "responsavel", (nome, email, vinculo.strip())
            )
            self.log(
                titular.evento_id,
                "consentimento_saude",
                "Autorização específica do responsável registrada.",
            )
        self.transacao.confirmar()
        return {"mensagem": "Decisão registrada. Este link não pode ser reutilizado."}
