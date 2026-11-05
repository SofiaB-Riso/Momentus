from application.erros import DadosInvalidos
from models import PlanejamentoEvento
from repositories.consulta_evento_repository import ConsultaEventoRepository
from repositories.lista_espera_repository import ListaEsperaRepository
from utils.validacao import validar_entrada

from services.caso_uso import CasoUso
from services.lista_espera.consultar_lista_espera_service import (
    ConsultarListaEsperaService,
)
from services.lista_espera.organizar_fila_service import OrganizarFilaService


class ConfigurarVagasService(CasoUso):
    def executar(self, evento_id, dados):
        dados = validar_entrada(dados)
        if "limite_vagas" not in dados:
            raise DadosInvalidos("Informe o limite de vagas ou null para desativar.")
        valor = dados["limite_vagas"]
        if valor is not None:
            if (
                isinstance(valor, bool)
                or not isinstance(valor, (str, int))
                or not str(valor).isdigit()
                or not 1 <= int(valor) <= 1000000
            ):
                raise DadosInvalidos(
                    "Informe de 1 a 1.000.000 vagas ou desative o limite."
                )
            valor = int(valor)
        _, evento = self.exigir_acesso_evento(evento_id, exigir_edicao=True)
        ConsultaEventoRepository.bloquear(evento.id)
        if valor is not None and valor < ListaEsperaRepository.confirmados(evento.id):
            raise DadosInvalidos(
                "O limite não pode ser menor que a quantidade já confirmada."
            )
        if not evento.planejamento:
            evento.planejamento = PlanejamentoEvento(evento_id=evento.id).salvar(
                confirmar=False
            )
        evento.planejamento.limite_vagas = valor
        OrganizarFilaService().promover(evento)
        self.log(
            evento.id,
            "vagas_configuradas",
            f"Limite: {valor if valor is not None else 'sem limite'}",
        )
        self.transacao.confirmar()
        return ConsultarListaEsperaService(self.transacao, self.usuario_id).executar(
            evento.id
        )
