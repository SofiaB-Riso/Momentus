# Arquitetura e qualidade do Momentus

Esta revisão usa como referência o projeto Flask/SQLAlchemy do professor: https://github.com/gleisonbt/projeto-flask-sqlalchemy. No exemplo do repositório, o fluxo é Controller → Service → Model para CRUD, com Repository nas consultas específicas e chamadas a stored procedures. Esse padrão foi mantido. Os materiais sobre procedures não foram interpretados como obrigação de reescrever todo o CRUD em SQL, pois o exemplo fornecido realiza o CRUD no Model.

## Fluxo de uma operação

O controller extrai o JSON ou formulário, identifica a conta autenticada e obtém o caso de uso pela composição da aplicação. O serviço valida as entradas, verifica a permissão e coordena entidades, consultas e histórico. Os models executam o CRUD sem confirmar a transação individualmente. A transação é confirmada quando o caso de uso termina; erros de aplicação ou de persistência recebidos pelo adaptador HTTP provocam rollback.

Exemplo: `controllers/evento_controller.py` delega a criação para `services/evento/criar_evento_service.py`. O serviço cria o evento e suas tarefas pelo CRUD dos models, grava o histórico e confirma tudo junto. `controllers/respostas.py` transforma o resultado em JSON com status 201 ou traduz os erros em respostas HTTP. Os serviços não importam Flask nem leem `request`, `session` ou `current_app`.

## Camadas

| Local | Responsabilidade | Exemplo |
|---|---|---|
| `backend/controllers` | Transporte HTTP e SSE; delegação para casos de uso | `convidados_controller.py` |
| `backend/services` | Regras de negócio e operações por recurso | `convidados/responder_rsvp_service.py` |
| `backend/models` | Entidades, relacionamentos, serialização básica e CRUD | `crud.py`, `evento_model.py` |
| `backend/repositories` | Persistência especializada e consultas | `item_repository.py`, `evento_repository.py` |
| `backend/application` | Contratos, composição e erros independentes de HTTP | `contratos.py`, `composicao.py` |
| `backend/infrastructure` | Implementações de integrações e efeitos externos | `provedores/google_places.py`, `exportadores/pdf.py` |
| `frontend` | Interface HTML/CSS/JavaScript consumindo as rotas existentes | `js/evento.js`, `js/api.js` |

O antigo controller que reunia convidados, tarefas, colaboração, financeiro, galeria e relatórios foi substituído por controllers por recurso e casos de uso com responsabilidades específicas. A serialização enriquecida e os cálculos financeiros ficam nos serviços, sem importar serviços nos models.

## SOLID aplicado

| Princípio | Aplicação concreta |
|---|---|
| Responsabilidade única (S) | HTTP nos controllers; regras nos serviços; arquivos físicos e exportação em implementações separadas. O rateio, RSVP, lembretes e relatórios possuem componentes próprios. |
| Aberto/fechado (O) | O serviço de relatório recebe um exportador. Um novo formato pode ser registrado na composição sem alterar o caso de uso. Estratégias de rateio são fornecidas por um registro de implementações. As rotas HTTP atuais continuam oferecendo PDF e Excel. |
| Substituição de Liskov (L) | Implementações estruturais dos contratos podem ser substituídas por provedores, repositórios, estratégias e exportadores alternativos. Os testes exercitam essas substituições sem alterar os casos de uso. |
| Segregação de interfaces (I) | Contratos pequenos para busca de fornecedores, fotos, arquivos, exportação, transação, consulta por tipo e estratégia de rateio. Um consumidor não precisa implementar operações que não usa. |
| Inversão de dependências (D) | Casos de uso recebem transação, armazenamento, provedor ou exportador. `application/composicao.py` escolhe Google, disco local, SQLAlchemy, PDF e Excel; os serviços não importam essas implementações de infraestrutura. |

Os serviços continuam usando os models e os repositórios especializados, como na arquitetura didática fornecida. Não foi introduzida uma abstração de repositório para cada entidade. SOLID orienta a separação onde há mudança real de responsabilidade ou implementação.

## Persistência e consistência

- `CrudModel` reúne salvar, buscar, listar, atualizar e deletar. Os casos de uso chamam essas operações com `confirmar=False`, mantendo evento, tarefas, avisos e histórico na mesma transação.
- `EventoRepository` utiliza `CALL sp_eventos_por_tipo` em MySQL e uma consulta equivalente em SQLite.
- Reservas concorrentes de itens usam atualização condicional atômica no repository, evitando atribuir o mesmo item simultaneamente a duas pessoas.
- Chaves estrangeiras estão ativas em SQLite e o SQL MySQL mantém os relacionamentos com exclusão em cascata ou desvínculo quando aplicável.
- Um upload é removido se sua gravação no banco falha. A substituição de comprovante remove o arquivo anterior após commit; exclusões de foto, despesa, evento e conta também limpam os arquivos relacionados após confirmação.
- A exclusão de uma conta libera suas responsabilidades de colaboração e preserva eventos de outras pessoas.

Banco e sistema de arquivos não compartilham uma transação distribuída. Uma falha de disco após commit ainda pode exigir limpeza manual do arquivo órfão. Os testes usam bancos temporários. O banco entregue foi esvaziado por solicitação do usuário e permanece sem registros.

## Compatibilidade

As 63 regras de rota e seus métodos HTTP foram mantidos. A limpeza centraliza a construção dos casos de uso em `controllers/contexto.py`, o acesso validado em `CasoUso.exigir_acesso_evento()` e o total financeiro em `Evento.total_despesas_decimal`. O streaming conserva a consulta de acesso que permite encerrar a conexão ao revogar permissões.

No frontend, `utils.js` e `localizacao-momentus.js` reúnem as funções compartilhadas, e os ícones idênticos usam uma só cópia por variante. A aparência e os fluxos foram comparados com a versão anterior. O SQLite padrão fica explicitamente em `backend/instance`, sem duplicação na raiz. Instalações MySQL continuam exigindo os procedimentos do script SQL; `create_all()` não os cria.

Esta revisão se concentra no projeto local. Permissões, commits e acesso ao repositório não foram alterados.
