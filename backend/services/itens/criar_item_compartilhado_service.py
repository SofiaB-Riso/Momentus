from application.contratos import Criado
from application.erros import Conflito, DadosInvalidos
from models import ItemCompartilhado
from repositories.consulta_evento_repository import ConsultaEventoRepository
from utils.validacao import inteiro_positivo, normalizar, validar_entrada

from services.caso_uso import CasoUso


class CriarItemCompartilhadoService(CasoUso):
    def executar(self, evento_id, dados=None):
        dados = validar_entrada(dados)
        _, evento = self.exigir_acesso_evento(evento_id, exigir_edicao=True)
        nome = " ".join(str(dados.get("nome") or "").split())
        if not nome or len(nome) > 160:
            raise DadosInvalidos("Informe o item com até 160 caracteres.")
        try:
            quantidade = inteiro_positivo(dados.get("quantidade", 1))
        except ValueError as erro:
            raise DadosInvalidos(str(erro))
        ConsultaEventoRepository.bloquear(evento.id, renovar=False)
        existe = next(
            (
                i
                for i in ItemCompartilhado.listar(evento_id=evento.id)
                if normalizar(i.nome) == normalizar(nome)
            ),
            None,
        )
        if existe:
            self.transacao.reverter()
            raise Conflito("Este item já está na lista.", item=existe.to_dict())
        item = ItemCompartilhado(evento_id=evento.id, nome=nome, quantidade=quantidade)
        item.salvar(confirmar=False)
        self.log(evento.id, "item_compartilhado_adicionado", nome)
        self.transacao.confirmar()
        return Criado(item.to_dict())
