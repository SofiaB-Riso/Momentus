from application.contratos import Criado
from application.erros import DadosInvalidos
from models import Convidado
from utils.validacao import validar_entrada

from services.caso_uso import CasoUso


class AdicionarConvidadoService(CasoUso):
    def executar(self, evento_id, dados=None):
        dados = validar_entrada(dados)
        usuario, evento = self.exigir_acesso_evento(evento_id, exigir_edicao=True)
        nome = (dados.get("nome") or "").strip()
        contato = (dados.get("contato") or "").strip()
        if not nome:
            raise DadosInvalidos("Nome do convidado é obrigatório.")
        email = (dados.get("email") or "").strip().lower()
        telefone = (dados.get("telefone") or "").strip()
        if contato:
            if "@" in contato and (not email):
                email = contato.lower()
            elif not telefone:
                telefone = contato
        if dados.get("status", "pendente") not in {
            "pendente",
            "confirmado",
            "recusado",
        }:
            raise DadosInvalidos("Status de presença inválido.")
        convidado = Convidado(
            evento_id=evento.id,
            nome=nome,
            email=email,
            telefone=telefone,
            vinculo=(dados.get("vinculo") or "").strip(),
            status=(dados.get("status") or "pendente").strip(),
            restricoes_alimentares=(
                dados.get("restricoes") or dados.get("restricoes_alimentares") or ""
            ).strip(),
        )
        convidado.salvar(confirmar=False)
        self.transacao.sincronizar()
        self.log(evento.id, "convidado_adicionado", convidado.nome)
        self.transacao.confirmar()
        resposta = convidado.to_dict()
        resposta["link_rsvp"] = f"/rsvp.html?token={convidado.token_rsvp}"
        return Criado(resposta)
