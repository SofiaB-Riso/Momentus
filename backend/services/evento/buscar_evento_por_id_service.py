from models import Evento
from services.caso_uso import CasoUso
from services.serializacao_evento import serializar_evento
from utils.validacao import validar_entrada


class BuscarEventoPorIdService(CasoUso):
    def executar(self, evento_id, dados=None):
        dados = validar_entrada(dados)
        usuario, evento = self.exigir_acesso_evento(evento_id)
        dados = self._preparar(evento_id)
        if evento.owner_id == usuario.id:
            dados["permissao"] = "dono"
            dados["pode_editar"] = True
        else:
            colab = next(
                (
                    c
                    for c in evento.colaboradores_rel
                    if c.usuario_id == usuario.id and c.status == "ativo"
                ),
                None,
            )
            dados["permissao"] = "colaborador"
            dados["pode_editar"] = bool(colab and colab.pode_editar)
            if not dados["pode_editar"]:
                for convidado in dados.get("lista_convidados", []):
                    convidado.pop("token_rsvp", None)
            for colaborador in dados.get("colaboradores", []):
                if colaborador["usuario_id"] != usuario.id:
                    colaborador.pop("token", None)
        return dados

    def _preparar(self, evento_id):
        evento = Evento.buscar_por_id(evento_id)
        return serializar_evento(evento) if evento else None
