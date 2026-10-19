from application.contratos import Criado
from application.erros import Conflito, DadosInvalidos, Proibido
from models import ColaboradorEvento, Notificacao
from repositories.usuario_repository import UsuarioRepository
from utils.validacao import validar_entrada

from services.caso_uso import CasoUso


class AdicionarColaboradorService(CasoUso):
    def executar(self, evento_id, dados=None):
        dados = validar_entrada(dados)
        usuario, evento = self.exigir_acesso_evento(evento_id)
        if evento.owner_id != usuario.id:
            raise Proibido(
                "Somente a pessoa dona do evento pode convidar colaboradores."
            )
        nome = (dados.get("nome") or "").strip()
        email = (dados.get("email") or dados.get("contato") or "").strip().lower()
        if not nome or "@" not in email:
            raise DadosInvalidos("Informe nome e e-mail do colaborador.")
        if email == usuario.email.lower():
            raise DadosInvalidos("Você já é a pessoa dona deste evento.")
        if ColaboradorEvento.buscar_um(evento_id=evento.id, email=email):
            raise Conflito("Esta pessoa já foi convidada para colaborar.")
        conta = UsuarioRepository.por_email(email)
        colab = ColaboradorEvento(
            evento_id=evento.id,
            usuario_id=conta.id if conta else None,
            nome=nome,
            email=email,
            status="pendente",
            pode_editar=bool(dados.get("pode_editar", True)),
        )
        colab.salvar(confirmar=False)
        self.transacao.sincronizar()
        if conta:
            Notificacao(
                usuario_id=conta.id,
                tipo="convite-colaborador",
                titulo="Convite para colaborar",
                mensagem=f"{usuario.nome} convidou você para colaborar em {evento.nome_evento}.",
                evento_id=evento.id,
                referencia_id=colab.id,
            ).salvar(confirmar=False)
        self.log(evento.id, "colaborador_convidado", email)
        self.transacao.confirmar()
        resposta = colab.to_dict()
        resposta["link_convite"] = f"/convite.html?token={colab.token}"
        resposta["possui_conta"] = bool(conta)
        return Criado(resposta)
