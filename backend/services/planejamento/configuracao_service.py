from application.erros import DadosInvalidos
from models import PlanejamentoEvento


class ConfigurarDuracaoService:
    def executar(self, evento, dados):
        if "duracao_minutos" not in dados:
            return
        valor = dados["duracao_minutos"]
        if (
            isinstance(valor, bool)
            or not isinstance(valor, (str, int))
            or not str(valor).isdigit()
            or not 15 <= int(valor) <= 1440
        ):
            raise DadosInvalidos("Informe a duração entre 15 e 1440 minutos.")
        config = evento.planejamento
        if not config:
            config = PlanejamentoEvento(evento_id=evento.id).salvar(confirmar=False)
            evento.planejamento = config
        config.duracao_minutos = int(valor)
