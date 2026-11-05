from application.contratos import Criado
from application.erros import Conflito, DadosInvalidos
from models import LocalEvento, LogEvento
from sqlalchemy.exc import IntegrityError
from utils.validacao import dinheiro, inteiro_positivo, normalizar, validar_entrada

from services.caso_uso import CasoUso


class SalvarLocalService(CasoUso):
    def executar(self, evento_id, dados=None):
        dados = validar_entrada(dados)
        usuario, evento = self.exigir_acesso_evento(evento_id, exigir_edicao=True)
        textos = {
            campo: str(dados.get(campo) or "").strip()
            for campo in ("nome", "endereco", "cidade", "estilo")
        }
        if not all(textos.values()) or any(
            (
                len(v) > limite
                for v, limite in zip(textos.values(), (180, 255, 120, 100))
            )
        ):
            raise DadosInvalidos(
                "Informe nome, endereço, cidade e estilo do espaço, respeitando o tamanho dos campos."
            )
        try:
            capacidade = inteiro_positivo(dados.get("capacidade"))
            preco = dinheiro(dados.get("preco"))
        except ValueError as erro:
            raise DadosInvalidos(str(erro))
        chave = normalizar(textos["nome"] + " " + textos["endereco"])[:255]
        local = LocalEvento(
            evento_id=evento.id,
            chave=chave,
            capacidade=capacidade,
            preco=preco,
            **textos,
        )
        local.salvar(confirmar=False)
        LogEvento(
            evento_id=evento.id,
            usuario_id=usuario.id,
            acao="local_adicionado",
            detalhe=local.nome,
        ).salvar(confirmar=False)
        try:
            self.transacao.confirmar()
        except IntegrityError:
            self.transacao.reverter()
            raise Conflito("Este espaço já está salvo para o evento.")
        return Criado(local.to_dict())
