import json

from application.contratos import ArquivoGerado
from models import Evento, FavoritoFornecedor, PrivacidadeUsuario
from models.tempo import utcnow

from services.caso_uso import CasoUso


class ExportarDadosService(CasoUso):
    def executar(self):
        usuario = self.usuario_atual(exigir_autorizacao=False)
        perfil = usuario.to_dict(incluir_fornecedor=False)
        if perfil.get("autorizacao_conta"):
            for campo in ("responsavel_nome", "responsavel_email"):
                perfil["autorizacao_conta"].pop(campo, None)
        registro = PrivacidadeUsuario.buscar_por_id(usuario.id)
        eventos = []
        for evento in Evento.listar(owner_id=usuario.id):
            dados = evento.to_dict(incluir_relacoes=False)
            # Observações e dados livres podem conter informações de terceiros.
            for campo in ("owner", "dados_evento", "observacoes"):
                dados.pop(campo, None)
            eventos.append(dados)
        dados = {
            "exportado_em": utcnow().isoformat() + "Z",
            "escopo": "Dados da conta, aceite, favoritos e informações básicas dos eventos criados. Sem anexos, senhas, tokens ou dados de convidados/colaboradores.",
            "conta": perfil,
            "aceite": registro.to_dict() if registro else None,
            "favoritos": [
                f.chave for f in FavoritoFornecedor.listar(usuario_id=usuario.id)
            ],
            "eventos_criados": eventos,
        }
        return ArquivoGerado(
            json.dumps(dados, ensure_ascii=False, indent=2).encode(),
            "meus-dados-momentus.json",
            "application/json",
        )
