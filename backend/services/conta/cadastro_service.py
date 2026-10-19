from application.contratos import Criado
from application.erros import Conflito, DadosInvalidos
from models import Usuario
from repositories.usuario_repository import UsuarioRepository
from utils.validacao import normalizar_email, validar_entrada

from services.caso_uso import CasoUso
from services.conta.convites_service import _vincular_convites_pendentes


class CadastroService(CasoUso):
    def executar(self, dados):
        dados = validar_entrada(dados)
        nome = (dados.get("nome") or "").strip()
        email = normalizar_email(dados.get("email"))
        senha = dados.get("senha") or ""
        telefone = (dados.get("telefone") or "").strip()
        if len(nome) < 2:
            raise DadosInvalidos("Informe seu nome completo.")
        if "@" not in email or "." not in email.split("@")[-1]:
            raise DadosInvalidos("Informe um e-mail válido.")
        if len(senha) < 6:
            raise DadosInvalidos("A senha precisa ter pelo menos 6 caracteres.")
        if UsuarioRepository.por_email(email):
            raise Conflito("Já existe uma conta com este e-mail.")
        usuario = Usuario(nome=nome, email=email, telefone=telefone, tipo="cliente")
        usuario.definir_senha(senha)
        usuario.salvar(confirmar=False)
        self.transacao.sincronizar()
        _vincular_convites_pendentes(usuario)
        self.transacao.confirmar()
        return Criado({"usuario": usuario.to_dict()})
