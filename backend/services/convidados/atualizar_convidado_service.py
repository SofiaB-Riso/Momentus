from application.erros import DadosInvalidos, NaoEncontrado
from models import Convidado
from repositories.consulta_evento_repository import ConsultaEventoRepository
from repositories.item_repository import ItemRepository
from utils.validacao import validar_entrada

from services.caso_uso import CasoUso
from services.convidados.informacoes_alimentares_service import (
    RegistrarInformacoesAlimentaresService,
)
from services.itens.liberacao_service import LiberarItensConvidadoService
from services.lista_espera.organizar_fila_service import OrganizarFilaService


class AtualizarConvidadoService(CasoUso):
    def executar(self, evento_id, convidado_id, dados=None):
        dados = validar_entrada(dados)
        _, evento = self.exigir_acesso_evento(evento_id, exigir_edicao=True)
        ConsultaEventoRepository.bloquear(evento.id)
        convidado = Convidado.buscar_um(id=convidado_id, evento_id=evento.id)
        if not convidado:
            raise NaoEncontrado("Convidado não encontrado.")
        if "nome" in dados and (not str(dados["nome"] or "").strip()):
            raise DadosInvalidos("O nome não pode ficar vazio.")
        if "status" in dados and dados["status"] not in {
            "pendente",
            "confirmado",
            "recusado",
        }:
            raise DadosInvalidos("Status de presença inválido.")
        for campo in ("nome", "email", "telefone", "vinculo"):
            if campo in dados:
                setattr(convidado, campo, (dados.get(campo) or "").strip())
        status = dados.get("status", convidado.status)
        RegistrarInformacoesAlimentaresService().executar(convidado, dados)
        if (
            status == "confirmado"
            and convidado.consentimento
            and convidado.consentimento.faixa_etaria == "menor"
            and convidado.consentimento.responsavel_autorizou is not True
        ):
            raise DadosInvalidos(
                "Aguarde a autorização do responsável para confirmar o menor."
            )
        if status == "recusado":
            RegistrarInformacoesAlimentaresService().executar(
                convidado, {"revogar_saude": True}
            )
            LiberarItensConvidadoService().executar(convidado)
        else:
            ItemRepository.atualizar_nome_convidado(convidado)
        if "status" in dados:
            OrganizarFilaService().aplicar(convidado, status)
        self.log(evento.id, "convidado_atualizado", convidado.nome)
        self.transacao.confirmar()
        return convidado.to_dict()
