from models import EntradaEspera
from models.tempo import utcnow
from repositories.lista_espera_repository import ListaEsperaRepository

from services.itens.liberacao_service import LiberarItensConvidadoService
from services.notificacoes_service import (
    AdicionarAvisoConvidadoService,
    NotificarOrganizacaoService,
)


class OrganizarFilaService:
    """Coordena presença e FIFO dentro da transação com o evento já bloqueado."""

    def cancelar(self, convidado):
        if convidado.entrada_espera:
            convidado.entrada_espera.ativo = False

    def aplicar(self, convidado, solicitado):
        evento = convidado.evento
        config = evento.planejamento
        if solicitado != "confirmado":
            convidado.status = solicitado
            self.cancelar(convidado)
            self.promover(evento)
            return
        # Quem já está confirmado não disputa novamente a própria vaga.
        if convidado.status == "confirmado":
            self.cancelar(convidado)
            return
        self.promover(evento)
        if convidado.status == "confirmado":
            self.cancelar(convidado)
            return
        limite = config.limite_vagas if config else None
        if limite is None or ListaEsperaRepository.confirmados(evento.id) < limite:
            convidado.status = "confirmado"
            self.cancelar(convidado)
            return
        convidado.status = "espera"
        LiberarItensConvidadoService().executar(convidado)
        entrada = convidado.entrada_espera
        if not entrada:
            entrada = EntradaEspera(
                evento_id=evento.id, convidado_id=convidado.id
            ).salvar(confirmar=False)
            convidado.entrada_espera = entrada
        if not entrada.ativo:
            entrada.solicitado_em = utcnow()
        entrada.ativo = True

    def promover(self, evento):
        config = evento.planejamento
        limite = config.limite_vagas if config else None
        confirmados = ListaEsperaRepository.confirmados(evento.id)
        for entrada in ListaEsperaRepository.fila(evento.id):
            if limite is not None and confirmados >= limite:
                break
            convidado = entrada.convidado
            consentimento = convidado.consentimento
            if (
                consentimento
                and consentimento.faixa_etaria == "menor"
                and consentimento.responsavel_autorizou is not True
            ):
                entrada.ativo = False
                convidado.status = "pendente"
                continue
            convidado.status = "confirmado"
            entrada.ativo = False
            confirmados += 1
            AdicionarAvisoConvidadoService().executar(
                convidado,
                "Sua vaga foi liberada",
                "Sua participação está confirmada. Confira os detalhes atualizados neste convite.",
                f"vaga:{entrada.id}:{entrada.solicitado_em.isoformat()}",
            )
            NotificarOrganizacaoService().executar(
                evento,
                "rsvp",
                "Vaga preenchida",
                f"{convidado.nome} saiu da lista de espera e teve a presença confirmada.",
                convidado.id,
            )
