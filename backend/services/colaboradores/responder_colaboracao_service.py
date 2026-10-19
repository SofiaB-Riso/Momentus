from application.erros import DadosInvalidos, NaoEncontrado, Proibido
from models import ColaboradorEvento, Notificacao
from repositories.consulta_evento_repository import ConsultaEventoRepository
from repositories.notificacao_repository import NotificacaoRepository
from utils.validacao import validar_entrada

from services.caso_uso import CasoUso
from services.itens.liberacao_service import liberar_itens_colaborador


class ResponderColaboracaoService(CasoUso):
    def executar(self, token, dados=None):
        dados = validar_entrada(dados)
        usuario = self.usuario_atual()
        colab = ColaboradorEvento.buscar_um(token=token)
        if not colab:
            raise NaoEncontrado("Convite de colaboração inválido.")
        if colab.email.lower() != usuario.email.lower():
            raise Proibido("Este convite foi enviado para outro e-mail.")
        status = dados.get("status")
        if status not in {"ativo", "recusado"}:
            raise DadosInvalidos("Resposta inválida.")
        ConsultaEventoRepository.bloquear(colab.evento_id)
        colab.usuario_id = usuario.id
        colab.nome = usuario.nome
        colab.status = status
        if status != "ativo":
            liberar_itens_colaborador(colab)
        NotificacaoRepository.responder_convite(usuario.id, colab.id)
        Notificacao(
            usuario_id=colab.evento.owner_id,
            tipo="colaborador-resposta",
            titulo="Resposta de colaborador",
            mensagem=f"{usuario.nome} {('aceitou' if status == 'ativo' else 'recusou')} colaborar em {colab.evento.nome_evento}.",
            evento_id=colab.evento_id,
            referencia_id=colab.id,
        ).salvar(confirmar=False)
        self.log(colab.evento_id, "colaborador_respondeu", f"{usuario.email}: {status}")
        self.transacao.confirmar()
        return colab.to_dict()
