from application.erros import DadosInvalidos, NaoEncontrado
from models import Convidado
from repositories.consulta_evento_repository import ConsultaEventoRepository
from repositories.item_repository import ItemRepository
from utils.validacao import validar_entrada

from services.caso_uso import CasoUso
from services.itens.liberacao_service import liberar_itens_convidado


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
        if "status" in dados and dados["status"] in {
            "pendente",
            "confirmado",
            "recusado",
        }:
            convidado.status = dados["status"]
        if "restricoes" in dados or "restricoes_alimentares" in dados:
            convidado.restricoes_alimentares = (
                dados.get("restricoes") or dados.get("restricoes_alimentares") or ""
            ).strip()
        if convidado.status == "recusado":
            liberar_itens_convidado(convidado)
        else:
            ItemRepository.atualizar_nome_convidado(convidado)
        self.log(evento.id, "convidado_atualizado", convidado.nome)
        self.transacao.confirmar()
        return convidado.to_dict()
