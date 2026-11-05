from datetime import date, datetime, timedelta

from application.erros import DadosInvalidos
from repositories.agenda_repository import AgendaRepository
from utils.validacao import normalizar, validar_entrada

from services.caso_uso import CasoUso


class VerificarConflitosAgendaService(CasoUso):
    def executar(self, dados):
        self.usuario_atual()
        dados = validar_entrada(dados)
        try:
            data = date.fromisoformat(dados.get("data_evento", ""))
        except (ValueError, TypeError):
            raise DadosInvalidos(
                "Informe uma data válida para verificar a agenda."
            ) from None
        hora = dados.get("hora_evento") or ""
        if not hora:
            raise DadosInvalidos(
                "Informe o horário para verificar sobreposição de eventos."
            )
        duracao = dados.get("duracao_minutos", 180)
        if (
            isinstance(duracao, bool)
            or not isinstance(duracao, (int, str))
            or not str(duracao).isdigit()
            or not 15 <= int(duracao) <= 1440
        ):
            raise DadosInvalidos("Informe a duração entre 15 e 1440 minutos.")
        try:
            inicio = datetime.fromisoformat(data.isoformat() + "T" + hora)
        except ValueError:
            raise DadosInvalidos("Informe um horário válido.") from None
        fim = inicio + timedelta(minutes=int(duracao))
        exceto = dados.get("evento_id")
        if exceto not in (None, ""):
            if isinstance(exceto, bool) or not str(exceto).isdigit():
                raise DadosInvalidos("Evento inválido.")
            exceto = int(exceto)
            self.exigir_acesso_evento(exceto)
        endereco = normalizar(dados.get("endereco_evento"))
        cidade = normalizar(dados.get("cidade_evento"))
        conflitos = []
        sem_horario = 0
        for evento in AgendaRepository.eventos_do_usuario(self.usuario_id, exceto):
            if not evento.hora_evento:
                if inicio.date() <= evento.data_evento <= fim.date():
                    sem_horario += 1
                continue
            outro_inicio = datetime.fromisoformat(
                evento.data_evento.isoformat() + "T" + evento.hora_evento
            )
            outro_fim = outro_inicio + timedelta(
                minutes=evento.planejamento.duracao_minutos
                if evento.planejamento
                else 180
            )
            if inicio < outro_fim and outro_inicio < fim:
                mesmo = bool(
                    endereco
                    and endereco == normalizar(evento.endereco_evento)
                    and cidade == normalizar(evento.cidade_evento)
                )
                conflitos.append(
                    {
                        "id": evento.id,
                        "nome": evento.nome_evento,
                        "inicio": outro_inicio.isoformat(),
                        "fim": outro_fim.isoformat(),
                        "mesmo_local": mesmo,
                        "motivos": ["Horários sobrepostos na sua agenda"]
                        + (["Mesmo endereço informado"] if mesmo else []),
                    }
                )
        conflitos.sort(key=lambda c: (c["inicio"], c["id"]))
        return {
            "inicio": inicio.isoformat(),
            "fim": fim.isoformat(),
            "conflitos": conflitos,
            "eventos_sem_horario": sem_horario,
            "escopo": "Seus eventos e eventos compartilhados com você. Endereços são comparados pelo texto; confirme a disponibilidade com o local. Eventos sem horário não permitem comparar intervalos.",
        }
