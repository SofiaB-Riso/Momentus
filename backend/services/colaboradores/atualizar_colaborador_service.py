from application.erros import DadosInvalidos, NaoEncontrado, Proibido
from models import ColaboradorEvento, Evento
from repositories.consulta_evento_repository import ConsultaEventoRepository
from repositories.notificacao_repository import NotificacaoRepository
from utils.validacao import validar_entrada

from services.caso_uso import CasoUso
from services.itens.liberacao_service import liberar_itens_colaborador


class AtualizarColaboradorService(CasoUso):
    def executar(self, evento_id, colaborador_id, dados=None):
        dados = validar_entrada(dados)
        usuario = self.usuario_atual()
        evento = Evento.buscar_por_id(evento_id)
        colab = ColaboradorEvento.buscar_um(id=colaborador_id, evento_id=evento_id)
        if not evento or not colab:
            raise NaoEncontrado("Convite não encontrado.")
        proprio = (
            colab.usuario_id == usuario.id
            and colab.email.lower() == usuario.email.lower()
        )
        if evento.owner_id != usuario.id and (not proprio):
            raise Proibido("Você não pode alterar este colaborador.")
        if "pode_editar" in dados and (not isinstance(dados["pode_editar"], bool)):
            raise DadosInvalidos("A permissão de edição deve ser verdadeira ou falsa.")
        ConsultaEventoRepository.bloquear(evento.id)
        if evento.owner_id == usuario.id:
            if "pode_editar" in dados:
                colab.pode_editar = bool(dados["pode_editar"])
            if dados.get("status") in {"pendente", "ativo", "recusado"}:
                colab.status = dados["status"]
        elif colab.usuario_id == usuario.id and dados.get("status") in {
            "ativo",
            "recusado",
        }:
            colab.status = dados["status"]
        else:
            raise Proibido("Você não pode alterar este colaborador.")
        if colab.status != "ativo":
            liberar_itens_colaborador(colab)
        if proprio and "status" in dados:
            NotificacaoRepository.responder_convite(usuario.id, colab.id)
        self.log(
            evento.id,
            "colaborador_atualizado",
            f"{colab.nome}: {colab.status}; {('pode editar' if colab.pode_editar else 'somente leitura')}",
        )
        self.transacao.confirmar()
        return colab.to_dict()
