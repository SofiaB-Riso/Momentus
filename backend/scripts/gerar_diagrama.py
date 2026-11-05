"""Gera as fontes UML e o inventário a partir das Models, sem abrir banco de dados."""

import json
import sys
from pathlib import Path

BACKEND = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BACKEND))
from models import db

DOCS = BACKEND.parent / "docs"
DIAGRAMAS = DOCS / "diagramas"
DIAGRAMAS.mkdir(parents=True, exist_ok=True)
MODELOS = {m.class_.__name__: m for m in db.Model.registry.mappers}
CAMPOS = {
    "PlanejamentoEvento": [
        "evento_id",
        "duracao_minutos",
        "limite_vagas",
        "cronograma_ativo",
        "cronograma_gerado_em",
    ],
    "PropostaFornecedor": [
        "id",
        "evento_id",
        "fornecedor",
        "categoria",
        "valor",
        "desconto",
        "taxas",
        "parcelas",
    ],
    "EntradaEspera": ["id", "evento_id", "convidado_id", "solicitado_em", "ativo"],
    "AutorizacaoConta": [
        "usuario_id",
        "faixa_etaria",
        "status",
        "versao",
        "autorizado_em",
        "revogado_em",
    ],
    "ConsentimentoAlimentar": [
        "convidado_id",
        "faixa_etaria",
        "saude",
        "versao",
        "autorizado_em",
        "revogado_em",
        "responsavel_autorizou",
    ],
    "PreferenciasUsuario": ["usuario_id", "rsvp", "lembretes"],
    "RequisicaoDespesa": [
        "id",
        "usuario_id",
        "evento_id",
        "despesa_id",
        "chave",
        "assinatura",
    ],
    "Usuario": ["id", "nome", "email", "senha_hash", "ativo"],
    "PrivacidadeUsuario": ["usuario_id", "foto_arquivo", "termos_versao", "aceito_em"],
    "RecuperacaoSenha": [
        "id",
        "usuario_id",
        "token_hash",
        "email",
        "expira_em",
        "usado_em",
    ],
    "Evento": [
        "id",
        "owner_id",
        "nome_evento",
        "tipo_evento",
        "data_evento",
        "orcamento_evento",
        "status",
    ],
    "ColaboradorEvento": [
        "id",
        "evento_id",
        "usuario_id",
        "nome",
        "email",
        "status",
        "pode_editar",
    ],
    "Convidado": [
        "id",
        "evento_id",
        "nome",
        "status",
        "restricoes_alimentares",
        "token_rsvp",
    ],
    "AvisoConvidado": ["id", "convidado_id", "chave", "titulo", "mensagem"],
    "ItemCompartilhado": [
        "id",
        "evento_id",
        "nome",
        "quantidade",
        "responsavel_tipo",
        "responsavel_id",
    ],
    "ItemEvento": ["id", "evento_id", "produto_id", "nome", "preco", "quantidade"],
    "TarefaEvento": ["id", "evento_id", "titulo", "feita", "prazo", "ordem"],
    "DespesaEvento": ["id", "evento_id", "descricao", "valor", "comprovante"],
    "FotoEvento": ["id", "evento_id", "usuario_id", "arquivo", "legenda"],
    "LocalEvento": [
        "id",
        "evento_id",
        "nome",
        "cidade",
        "capacidade",
        "preco",
        "estilo",
    ],
    "Fornecedor": [
        "id",
        "usuario_id",
        "nome_empresa",
        "tipo_servico",
        "cidade",
        "avaliacao",
    ],
    "ProdutoFornecedor": ["id", "fornecedor_id", "nome", "categoria", "preco", "ativo"],
    "FavoritoFornecedor": ["id", "usuario_id", "chave"],
    "Notificacao": ["id", "usuario_id", "evento_id", "tipo", "titulo", "lida"],
    "LogEvento": ["id", "evento_id", "usuario_id", "acao", "detalhe", "criado_em"],
}
VISOES = [
    (
        "10-propostas",
        "Propostas de fornecedores",
        ["Evento", "PropostaFornecedor"],
        ['Evento "1" *-- "0..*" PropostaFornecedor : orcamentos recebidos'],
    ),
    (
        "11-planejamento-fila",
        "Planejamento, cronograma e espera",
        ["Evento", "PlanejamentoEvento", "EntradaEspera", "Convidado", "TarefaEvento"],
        [
            'Evento "1" *-- "0..1" PlanejamentoEvento : duracao vagas e cronograma',
            'Evento "1" *-- "0..*" EntradaEspera : fila',
            'Convidado "1" *-- "0..1" EntradaEspera : solicitacao',
            'Evento "1" *-- "0..*" TarefaEvento : etapas manuais e geradas',
        ],
    ),
    (
        "08-autorizacoes",
        "Autorizações e dados alimentares",
        ["Usuario", "AutorizacaoConta", "Convidado", "ConsentimentoAlimentar"],
        [
            'Usuario "1" *-- "0..1" AutorizacaoConta : declaracao e responsavel',
            'Convidado "1" *-- "0..1" ConsentimentoAlimentar : preferencias e saude',
        ],
    ),
    (
        "09-preferencias-envios",
        "Preferências e proteção de envios",
        [
            "Usuario",
            "PreferenciasUsuario",
            "Evento",
            "DespesaEvento",
            "RequisicaoDespesa",
        ],
        [
            'Usuario "1" *-- "0..1" PreferenciasUsuario : notificacoes',
            'Usuario "1" *-- "0..*" RequisicaoDespesa : reenvios',
            'Evento "1" *-- "0..*" RequisicaoDespesa : contexto',
            'DespesaEvento "0..1" <-- "0..*" RequisicaoDespesa : resultado',
        ],
    ),
    (
        "07-conta-privacidade",
        "Conta, aceite e recuperação",
        ["Usuario", "PrivacidadeUsuario", "RecuperacaoSenha"],
        [
            'Usuario "1" *-- "0..1" PrivacidadeUsuario : perfil e aceite',
            'Usuario "1" *-- "0..*" RecuperacaoSenha : links de recuperacao',
        ],
    ),
    (
        "01-heranca",
        "Herança e persistência",
        ["Usuario", "Evento"],
        [
            "CrudModel <|-- Usuario",
            "SQLAlchemyModel <|-- Usuario",
            "CrudModel <|-- Evento",
            "SQLAlchemyModel <|-- Evento",
        ],
    ),
    (
        "02-organizacao",
        "Contas, organização e convidados",
        ["Usuario", "Evento", "ColaboradorEvento", "Convidado", "AvisoConvidado"],
        [
            'Usuario "1" --> "0..*" Evento : cria',
            'Evento "1" *-- "0..*" ColaboradorEvento : participantes',
            'Usuario "0..1" o-- "0..*" ColaboradorEvento : vinculo de conta',
            'Evento "1" *-- "0..*" Convidado : convidados',
            'Convidado "1" *-- "0..*" AvisoConvidado : avisos',
        ],
    ),
    (
        "03-itens-tarefas",
        "Itens e tarefas do evento",
        [
            "Evento",
            "ItemCompartilhado",
            "ItemEvento",
            "TarefaEvento",
            "ProdutoFornecedor",
        ],
        [
            'Evento "1" *-- "0..*" ItemCompartilhado : lista compartilhada',
            'Evento "1" *-- "0..*" ItemEvento : itens contratados',
            'Evento "1" *-- "0..*" TarefaEvento : checklist',
            'ProdutoFornecedor "0..1" o-- "0..*" ItemEvento : origem opcional',
        ],
    ),
    (
        "04-financeiro-galeria",
        "Despesas, fotos e locais",
        ["Evento", "DespesaEvento", "FotoEvento", "LocalEvento", "Usuario"],
        [
            'Evento "1" *-- "0..*" DespesaEvento : despesas',
            'Evento "1" *-- "0..*" FotoEvento : galeria',
            'Evento "1" *-- "0..*" LocalEvento : espacos salvos',
            'Usuario "0..1" o-- "0..*" FotoEvento : autoria opcional',
        ],
    ),
    (
        "05-fornecedores-favoritos",
        "Catálogo legado e favoritos",
        ["Usuario", "Fornecedor", "ProdutoFornecedor", "FavoritoFornecedor"],
        [
            'Usuario "1" *-- "0..1" Fornecedor : perfil comercial legado',
            'Fornecedor "1" *-- "0..*" ProdutoFornecedor : produtos',
            'Usuario "1" *-- "0..*" FavoritoFornecedor : favoritos',
        ],
    ),
    (
        "06-notificacoes-historico",
        "Notificações e histórico",
        ["Usuario", "Evento", "Notificacao", "LogEvento"],
        [
            'Usuario "1" --> "0..*" Notificacao : destinatario',
            'Evento "0..1" --> "0..*" Notificacao : contexto opcional',
            'Evento "1" *-- "0..*" LogEvento : historico',
            'Usuario "0..1" --> "0..*" LogEvento : autoria opcional',
        ],
    ),
]


def tipo(coluna):
    nome = str(coluna.type)
    for prefixo, resultado in [
        ("INTEGER", "int"),
        ("VARCHAR", "String"),
        ("TEXT", "String"),
        ("BOOLEAN", "bool"),
        ("DATETIME", "DateTime"),
        ("DATE", "Date"),
        ("NUMERIC", "Decimal"),
    ]:
        if nome.startswith(prefixo):
            return resultado
    return nome.split("(")[0]


def inventario():
    return {
        nome: {
            "tabela": m.local_table.name,
            "arquivo": str(
                Path(sys.modules[m.class_.__module__].__file__)
                .resolve()
                .relative_to(BACKEND)
            ),
            "heranca": ["CrudModel", "db.Model"],
            "atributos": {
                c.name: {
                    "tipo_sql": str(c.type),
                    "nullable": c.nullable,
                    "pk": c.primary_key,
                }
                for c in m.local_table.columns
            },
            "chaves_estrangeiras": sorted(
                [
                    {
                        "campo": fk.parent.name,
                        "alvo": fk.target_fullname,
                        "ondelete": fk.ondelete,
                    }
                    for fk in m.local_table.foreign_keys
                ],
                key=lambda f: f["campo"],
            ),
        }
        for nome, m in sorted(MODELOS.items())
    }


def main():
    assert set(CAMPOS) == set(MODELOS)
    texto = [
        "# Diagrama de classes do domínio",
        "",
        f"As {len(VISOES)} vistas abaixo representam as {len(MODELOS)} entidades implementadas em `backend/models`. Uma classe repetida em vistas diferentes continua sendo a mesma entidade. Os atributos mostrados são os principais; o inventário completo está em [modelos.json](modelos.json).",
        "",
        "Todas as entidades herdam de `CrudModel` e `db.Model` por herança múltipla. A primeira vista mostra essa estrutura com Usuario e Evento; ela também se aplica às demais entidades. No desenho, SQLAlchemyModel representa `db.Model`, não uma entidade adicional do domínio.",
        "",
        "**Legenda UML:** triângulo vazio = herança; losango preenchido = composição (parte dependente do ciclo de vida do todo); losango vazio = agregação (vínculo compartilhado/opcional); seta simples = associação. Cardinalidades indicam quantos registros podem participar de cada vínculo.",
        "",
        "As composições consideram as relações `delete-orphan` e/ou chaves estrangeiras com exclusão em cascata. Autoria e origem opcionais com `SET NULL` são vínculos independentes: excluir a conta ou produto não apaga automaticamente a parte mantida por outro evento.",
        "",
    ]
    for arquivo, titulo, classes, relacoes in VISOES:
        fonte = ["classDiagram", "direction TB"]
        if arquivo == "01-heranca":
            fonte += [
                "class SQLAlchemyModel",
                "class CrudModel {",
                "    +salvar()",
                "    +atualizar(campos)",
                "    +deletar()",
                "    +listar_todos()",
                "    +buscar_por_id(id)",
                "}",
            ]
        for nome in classes:
            fonte += ["class " + nome + " {"]
            for campo in CAMPOS[nome]:
                coluna = MODELOS[nome].local_table.columns[campo]
                fonte.append("    +" + tipo(coluna) + " " + campo)
            fonte += ["}"]
        fonte += relacoes
        (DIAGRAMAS / (arquivo + ".mmd")).write_text("\n".join(fonte) + "\n")
        texto += [
            "## " + titulo,
            "",
            f"![{titulo}](diagramas/{arquivo}.svg)",
            "",
            f"[Fonte Mermaid](diagramas/{arquivo}.mmd)",
            "",
        ]
    texto += [
        "## Precisões sobre o modelo",
        "",
        "- `responsavel_tipo`/`responsavel_id` de ItemCompartilhado são uma referência lógica validada pelos Services, sem chave estrangeira polimórfica; não foi inventada uma associação ORM no desenho.",
        "- `FavoritoFornecedor.chave` identifica um estabelecimento externo ou legado. Não existe FK direta desse campo para Fornecedor.",
        "- `Notificacao.referencia_id` é uma referência contextual, não uma FK para uma única entidade.",
        "- As entidades Fornecedor e ProdutoFornecedor mantêm o catálogo legado e seus dados relacionais; o cadastro comercial de fornecedor não integra a lista de 40 funcionalidades da interface atual.",
        "",
        "## Atualização",
        "",
        "Na pasta backend, execute `py scripts/gerar_diagrama.py` (ou python3). O script lê os metadados das Models sem abrir banco e regenera as fontes/inventário. Os SVGs podem ser exportados com Mermaid CLI. Os testes verificam a correspondência do inventário e dos atributos com as Models.",
        "",
    ]
    (DOCS / "diagrama_classes.md").write_text("\n".join(texto))
    (DOCS / "modelos.json").write_text(
        json.dumps(inventario(), ensure_ascii=False, indent=2) + "\n"
    )
    print(
        f"Diagrama: {len(MODELOS)} Models, {len(VISOES)} vistas e inventário gerados sem acessar banco."
    )


if __name__ == "__main__":
    main()
