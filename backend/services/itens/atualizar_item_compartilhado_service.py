from application.erros import Conflito, DadosInvalidos, NaoEncontrado
from models import ColaboradorEvento, ItemCompartilhado
from repositories.consulta_evento_repository import ConsultaEventoRepository
from repositories.item_repository import ItemRepository
from utils.validacao import inteiro_positivo, validar_entrada

from services.caso_uso import CasoUso


class AtualizarItemCompartilhadoService(CasoUso):
    def executar(self, evento_id, item_id, dados=None):
        dados = validar_entrada(dados)
        usuario, evento = self.exigir_acesso_evento(evento_id, exigir_edicao=True)
        ConsultaEventoRepository.bloquear(evento.id)
        item = ItemCompartilhado.buscar_um(id=item_id, evento_id=evento.id)
        if not item:
            raise NaoEncontrado("Item não encontrado.")
        valores = {}
        if "quantidade" in dados:
            try:
                valores["quantidade"] = inteiro_positivo(dados["quantidade"])
            except ValueError as erro:
                raise DadosInvalidos(str(erro))
        pessoa = None
        tipo = None
        if dados.get("liberar"):
            valores.update(
                responsavel_tipo=None, responsavel_id=None, responsavel_nome=""
            )
        elif "responsavelNome" in dados or "responsavel_nome" in dados:
            tipo = dados.get("responsavelTipo") or "usuario"
            pessoa_id = dados.get("responsavelId")
            if tipo == "colaborador":
                pessoa = ColaboradorEvento.buscar_um(
                    id=pessoa_id, evento_id=evento.id, status="ativo"
                )
            elif tipo == "convidado":
                pessoa = ItemRepository.convidado_participante(pessoa_id, evento.id)
            elif tipo == "usuario":
                pessoa = usuario
            else:
                pessoa = None
            if not pessoa:
                raise DadosInvalidos("Escolha uma pessoa participante deste evento.")
            valores.update(
                responsavel_tipo=tipo,
                responsavel_id=pessoa.id,
                responsavel_nome=pessoa.nome,
            )
        if valores and (
            not ItemRepository.atualizar_reserva(
                item.id, evento.id, valores, pessoa, tipo
            )
        ):
            self.transacao.reverter()
            raise Conflito("Este item já tem responsável. Libere-o antes de trocar.")
        self.log(
            evento.id,
            "item_compartilhado_atualizado",
            f"{item.nome}: {item.quantidade} unidade(s); {item.responsavel_nome or 'sem responsável'}",
        )
        self.transacao.confirmar()
        return item.to_dict()
