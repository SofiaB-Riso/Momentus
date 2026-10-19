from datetime import date

from application.erros import DadosInvalidos, Proibido
from models import Evento
from repositories.consulta_evento_repository import ConsultaEventoRepository
from services.caso_uso import CasoUso
from services.notificacoes_service import avisar_convidados, notificar_organizacao
from services.serializacao_evento import serializar_evento
from sqlalchemy.exc import SQLAlchemyError
from utils.validacao import dinheiro, validar_entrada


class AtualizarEventoService(CasoUso):
    def executar(self, evento_id, dados=None):
        dados = validar_entrada(dados)
        usuario, evento = self.exigir_acesso_evento(evento_id, exigir_edicao=True)
        try:
            if (
                "privacidade_convidados" in dados
                and dados["privacidade_convidados"] != evento.privacidade_convidados
                and (usuario.id != evento.owner_id)
            ):
                raise Proibido(
                    "Somente a pessoa dona do evento pode alterar a privacidade."
                )
            antes = {
                "data": evento.data_evento.isoformat() if evento.data_evento else "",
                "hora": evento.hora_evento or "",
                "local": evento.endereco_evento or "",
                "cidade": evento.cidade_evento or "",
            }
            atualizado = self._preparar(evento_id, dados)
            mudancas = []
            if atualizado.get("data_evento", "") != antes["data"]:
                mudancas.append("data")
            if atualizado.get("hora_evento", "") != antes["hora"]:
                mudancas.append("horário")
            if (
                atualizado.get("endereco_evento", "") != antes["local"]
                or atualizado.get("cidade_evento", "") != antes["cidade"]
            ):
                mudancas.append("local")
            self.log(
                evento_id,
                "evento_atualizado",
                ", ".join(mudancas) if mudancas else "dados gerais",
            )
            if mudancas:
                mensagem = f"{evento.nome_evento}: alteração de {', '.join(mudancas)}. Data: {evento.data_evento.strftime('%d/%m/%Y')}, {evento.hora_evento or 'horário a confirmar'}. Local: {evento.endereco_evento}, {evento.cidade_evento}."
                notificar_organizacao(
                    evento,
                    "evento-alterado",
                    "Evento atualizado",
                    mensagem,
                    exceto=usuario.id,
                )
                self.transacao.sincronizar()
                ultimo_log = ConsultaEventoRepository.ultimo_log(evento.id)
                avisar_convidados(
                    evento,
                    "Os detalhes do evento mudaram",
                    mensagem,
                    f"alteracao:{ultimo_log.id}",
                )
            self.transacao.confirmar()
            return serializar_evento(evento)
        except ValueError as erro_valor:
            self.transacao.reverter()
            raise DadosInvalidos(str(erro_valor))
        except SQLAlchemyError:
            self.transacao.reverter()
            raise

    def _preparar(self, evento_id, dados):
        dados = validar_entrada(dados)
        evento = Evento.buscar_por_id(evento_id)
        if evento is None:
            return None
        mapeamento_texto = {
            "nome_evento": "nome_evento",
            "tipo_evento": "tipo_evento",
            "hora_evento": "hora_evento",
            "endereco_evento": "endereco_evento",
            "cidade_evento": "cidade_evento",
            "estilo_evento": "estilo_evento",
            "observacoes": "observacoes",
            "status": "status",
            "privacidade_convidados": "privacidade_convidados",
            "dados_evento": "dados_evento",
        }
        for entrada, atributo in mapeamento_texto.items():
            if entrada in dados:
                setattr(
                    evento,
                    atributo,
                    dados.get(entrada)
                    if entrada == "dados_evento"
                    else (dados.get(entrada) or "").strip(),
                )
        if dados.get("data_evento"):
            try:
                evento.data_evento = date.fromisoformat(dados["data_evento"])
            except ValueError:
                raise ValueError("'data_evento' deve estar no formato AAAA-MM-DD.")
        if "orcamento_evento" in dados:
            evento.orcamento_evento = dinheiro(dados.get("orcamento_evento") or 0)
        if "convidados_estimados" in dados:
            evento.convidados_estimados = max(
                0, int(dados.get("convidados_estimados") or 0)
            )
        if "progresso" in dados:
            evento.progresso = max(0, min(100, int(dados.get("progresso") or 0)))
        if "rateio" in dados and isinstance(dados["rateio"], dict):
            rateio = dados["rateio"]
            if "ativo" in rateio:
                if not isinstance(rateio["ativo"], bool):
                    raise ValueError("Ativo deve ser verdadeiro ou falso.")
                evento.rateio_ativo = bool(rateio["ativo"])
            if "modo" in rateio:
                if rateio["modo"] not in {"auto", "fixo"}:
                    raise ValueError("Modo de rateio inválido.")
                evento.rateio_modo = rateio["modo"]
            if "valorFixo" in rateio:
                evento.rateio_valor_fixo = dinheiro(rateio.get("valorFixo") or 0)
        if evento.privacidade_convidados not in {"todos", "organizador"}:
            raise ValueError("Privacidade inválida.")
        self.transacao.sincronizar()
        return serializar_evento(evento)
