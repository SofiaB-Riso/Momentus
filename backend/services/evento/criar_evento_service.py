from datetime import date

from application.contratos import Criado
from application.erros import DadosInvalidos
from models import Evento, TarefaEvento
from services.caso_uso import CasoUso
from services.serializacao_evento import serializar_evento
from sqlalchemy.exc import SQLAlchemyError
from utils.validacao import dinheiro, validar_entrada

TAREFAS_PADRAO = [
    ("checklistLocal", "Escolha o local"),
    ("checklistCardapio", "Defina o cardápio"),
    ("checklistConvites", "Envie os convites"),
    ("checklistFornecedores", "Confirme os fornecedores"),
]


class CriarEventoService(CasoUso):
    def executar(self, dados=None):
        dados = validar_entrada(dados)
        try:
            usuario = self.usuario_atual()
            evento = self._preparar(dados, usuario.id)
            self.log(evento["id"], "evento_criado", evento["nome_evento"])
            self.transacao.confirmar()
            return Criado(serializar_evento(Evento.buscar_por_id(evento["id"])))
        except ValueError as erro:
            self.transacao.reverter()
            raise DadosInvalidos(str(erro))
        except SQLAlchemyError:
            self.transacao.reverter()
            raise

    def _preparar(self, dados, owner_id):
        dados = validar_entrada(dados)
        for campo in ("nome_evento", "tipo_evento", "data_evento"):
            valor = dados.get(campo)
            if valor is None or (isinstance(valor, str) and (not valor.strip())):
                raise ValueError(f"O campo '{campo}' é obrigatório.")
        try:
            data_evento = date.fromisoformat(dados["data_evento"])
        except (TypeError, ValueError):
            raise ValueError("'data_evento' deve estar no formato AAAA-MM-DD.")
        evento = Evento(
            owner_id=owner_id,
            nome_evento=str(dados["nome_evento"]).strip(),
            tipo_evento=str(dados["tipo_evento"]).strip(),
            data_evento=data_evento,
            hora_evento=(dados.get("hora_evento") or "").strip(),
            endereco_evento=(dados.get("endereco_evento") or "").strip(),
            cidade_evento=(dados.get("cidade_evento") or "").strip(),
            orcamento_evento=dinheiro(dados.get("orcamento_evento") or 0),
            convidados_estimados=max(0, int(dados.get("convidados_estimados") or 0)),
            estilo_evento=(dados.get("estilo_evento") or "").strip(),
            observacoes=(dados.get("observacoes") or "").strip(),
            status=(dados.get("status") or "agendado").strip(),
            progresso=max(0, min(100, int(dados.get("progresso") or 0))),
            privacidade_convidados=(
                dados.get("privacidade_convidados") or "organizador"
            ).strip(),
            dados_evento=dados.get("dados_evento"),
        )
        if evento.privacidade_convidados not in {"todos", "organizador"}:
            raise ValueError("Privacidade inválida.")
        evento.salvar(confirmar=False)
        self.transacao.sincronizar()
        for ordem, (chave, titulo) in enumerate(TAREFAS_PADRAO):
            TarefaEvento(
                evento_id=evento.id, chave=chave, titulo=titulo, ordem=ordem
            ).salvar(confirmar=False)
        self.transacao.sincronizar()
        return serializar_evento(evento)
