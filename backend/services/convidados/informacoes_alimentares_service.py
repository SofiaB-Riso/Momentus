from application.erros import DadosInvalidos
from models import ConsentimentoAlimentar
from models.tempo import utcnow

from services.conta.termos import VERSAO_TERMOS


class RegistrarInformacoesAlimentaresService:
    """O organizador informa preferências; saúde vem do titular ou responsável."""

    def executar(self, convidado, dados, origem="organizador", responsavel=None):
        campos = {
            "restricoes",
            "restricoes_alimentares",
            "saude",
            "revogar_saude",
            "faixa_etaria",
        }
        if not campos.intersection(dados):
            return
        registro = convidado.consentimento
        if registro is None:
            registro = ConsentimentoAlimentar(convidado_id=convidado.id).salvar(
                confirmar=False
            )
            convidado.consentimento = registro
        if "restricoes" in dados or "restricoes_alimentares" in dados:
            texto = (
                dados.get("restricoes") or dados.get("restricoes_alimentares") or ""
            ).strip()
            if (
                texto
                and registro.faixa_etaria == "menor"
                and registro.responsavel_autorizou is not True
            ):
                raise DadosInvalidos(
                    "Aguarde a autorização do responsável para informar preferências do menor."
                )
            if texto and dados.get("preferencias_sem_saude") is not True:
                raise DadosInvalidos(
                    "Confirme que as preferências não incluem informações de saúde. Alergias devem ser informadas pelo titular ou responsável no RSVP."
                )
            convidado.restricoes_alimentares = texto
            registro.preferencias_sem_saude = True
        if "faixa_etaria" in dados:
            if origem == "organizador" or dados["faixa_etaria"] not in {
                "adulto",
                "menor",
            }:
                raise DadosInvalidos(
                    "A idade deve ser declarada pelo titular no convite."
                )
            if registro.faixa_etaria == "menor" and dados["faixa_etaria"] != "menor":
                raise DadosInvalidos(
                    "Use o canal de privacidade para corrigir a declaração de idade."
                )
            registro.faixa_etaria = dados["faixa_etaria"]
        if dados.get("revogar_saude") is True or (
            "saude" in dados and not dados["saude"]
        ):
            registro.saude = ""
            registro.revogado_em = utcnow()
            registro.token_hash = None
            registro.expira_em = None
            return
        if "saude" not in dados:
            return
        saude = dados.get("saude")
        if not isinstance(saude, str) or len(saude.strip()) > 4000:
            raise DadosInvalidos(
                "Descreva somente os cuidados alimentares necessários, em até 4000 caracteres."
            )
        if origem not in {"rsvp", "responsavel"}:
            raise DadosInvalidos(
                "Informações de saúde devem ser fornecidas pelo próprio convidado ou responsável no convite."
            )
        if origem == "rsvp" and registro.faixa_etaria != "adulto":
            raise DadosInvalidos(
                "Para menores, gere o link e peça a autorização do responsável."
            )
        if (
            dados.get("autorizar_saude") is not True
            or dados.get("versao_consentimento") != VERSAO_TERMOS
        ):
            raise DadosInvalidos(
                "É necessária autorização específica para registrar informações de saúde."
            )
        registro.saude = saude.strip()
        registro.autorizado_em = utcnow()
        registro.revogado_em = None
        registro.versao = VERSAO_TERMOS
        registro.origem = origem
        if origem == "responsavel" and registro.responsavel_autorizou is not True:
            raise DadosInvalidos(
                "O responsável precisa autorizar os dados da participação antes de fornecer saúde."
            )
        if responsavel:
            registro.responsavel_nome, registro.responsavel_email, registro.vinculo = (
                responsavel
            )
