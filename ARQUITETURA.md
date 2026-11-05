# Arquitetura e qualidade do Momentus

Esta revisão segue o enunciado da disciplina fornecido pelo grupo: Controller → Service → Model para CRUD, com Repository nas consultas específicas e chamadas a stored procedures. O repositório indicado pelo professor é https://github.com/gleisonbt/projeto-flask-sqlalchemy. As exigências adotadas nesta revisão são as do enunciado transcrito, incluindo CRUD nas Models e Repository para operações especiais.

## Fluxo de uma operação

Cada Controller é uma classe por recurso. Seus métodos extraem o JSON ou formulário, identificam a conta autenticada e obtêm o caso de uso pela composição da aplicação. O registro dos métodos nos Blueprints fica em `controllers/registro.py`; os Blueprints organizam as rotas, e a implementação HTTP pertence às classes. O serviço valida as entradas, verifica a permissão e coordena entidades, consultas e histórico. Os models executam o CRUD sem confirmar a transação individualmente. A transação é confirmada quando o caso de uso termina; erros de aplicação ou de persistência recebidos pelo adaptador HTTP provocam rollback.

Exemplo: `EventoController.criar_evento()` em `controllers/evento_controller.py` delega a criação para `services/evento/criar_evento_service.py`. O serviço cria o evento e suas tarefas pelo CRUD dos models, grava o histórico e confirma tudo junto. `controllers/respostas.py` transforma o resultado em JSON com status 201 ou traduz os erros em respostas HTTP. Os serviços não importam Flask nem leem `request`, `session` ou `current_app`.

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

Na revisão de 05/11, ConsultaEventoRepository.metadados consulta a revisão e o primeiro instante da ação evento_criado em uma única agregação. serializacao_evento enriquece o DTO com criado_em em UTC. A data não é inventada a partir da data da festa e não exige alterar a Model Evento ou migrar o banco. A formatação relativa e a atualização do texto dos ingressos são responsabilidades de apresentação em frontend/js/utils.js e script.js. planejar-interface.js e evento-interface.js cuidam da prévia, destaques e navegação visual; persistência e permissões continuam nos fluxos da API.

## SOLID aplicado

O acabamento comum das 15 páginas está em frontend/css/acabamento.css, carregado depois dos estilos compartilhados e específicos. As páginas de termos e privacidade organizam o conteúdo existente com um índice nativo de âncoras; os textos e PDFs são preservados. recuperacao.js controla a apresentação e chama as mesmas rotas de autenticação, mantendo regras de token, validade, troca de senha e persistência nos Services existentes. A preparação do ZIP vazio cria o esquema atual sem registros; não introduz limpeza de dados na inicialização do aplicativo.

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

Banco e sistema de arquivos não compartilham uma transação distribuída. Uma falha de disco após commit ainda pode exigir limpeza manual do arquivo órfão. Os testes usam bancos temporários. A revisão de interface preserva o banco e os anexos recebidos no ZIP mais recente do grupo.

## Compatibilidade

As rotas anteriores foram mantidas, com novas ações de preferências, CSRF e autorizações. A composição fica em `controllers/contexto.py`, o acesso validado em `CasoUso.exigir_acesso_evento()` e o total financeiro em `Evento.total_despesas_decimal`. O streaming encerra a conexão ao revogar permissões ou a autorização de uma conta de menor.

No frontend, `utils.js` e `localizacao-momentus.js` reúnem as funções compartilhadas, e os ícones idênticos usam uma só cópia por variante. A aparência e os fluxos foram comparados com a versão anterior. O SQLite padrão fica explicitamente em `backend/instance`, sem duplicação na raiz. Instalações MySQL continuam exigindo os procedimentos do script SQL; `create_all()` não os cria.

Esta revisão se concentra no projeto local. Permissões, commits e acesso ao repositório não foram alterados.

## Adequação ao enunciado da disciplina

- As rotas próprias são métodos de instâncias de Controllers, incluindo autenticação, recursos do evento, SSE e arquivos da interface. Nenhuma regra de negócio foi movida para o registro das rotas.
- Os casos de uso e os auxiliares de regras de negócio são classes com executar(). Cada classe tem uma ação; validação pura e formatação podem ser funções auxiliares.
- As 25 Models ficam em arquivos próprios e herdam de CrudModel e db.Model. CrudModel fornece salvar, atualizar, deletar, listar_todos e buscar_por_id; listar(**campos) permanece como consulta simples compatível.
- A busca e a foto legada do Google são Services específicos em services/integracoes. O provider apenas adapta os contratos; o HTTP externo não fica nas Controllers nem nos Repositories.
- Os 40 casos da matriz documentam tela → API → Controller em classe → Service → Model/Repository → banco. Temas, animações e buscas exclusivamente externas são recursos complementares, sem inflar essa lista.
- O diagrama em docs/diagrama_classes.md e seu inventário são gerados a partir das Models. Os testes verificam a coerência dos atributos, chaves estrangeiras e heranças.

## Correções da auditoria

Autorizações de conta e alimentação são casos de uso próprios; tokens de responsáveis são armazenados como hash, expiram e são consumidos por atualização condicional no Repository. O acesso ao evento verifica a autorização da conta e sua permissão específica. Não há confiança automática no e-mail de uma conta nova para aceitar convites pendentes.

O cadastro de despesa recebe uma chave UUID por envio; a conta e o evento são bloqueados antes de consultar a chave e persistir despesa, histórico e registro de idempotência na mesma transação. Reenvios equivalentes retornam o lançamento original; reutilização com outro conteúdo retorna conflito. A interface bloqueia envios concorrentes e permite reenviar somente o comprovante.

A remoção física de arquivos confirma prefixo do recurso e ausência de outras referências após commit. Validação de JSON/HTTP fica no adaptador; regras de campos, status e consentimento ficam nos Services. CSRF, cabeçalhos, limites HTTP e configuração de produção são infraestrutura, sem dependência de Flask nos Services. Veja [operação](docs/OPERACAO.md) para o alcance e os limites dessas proteções.


A extensão de 03/11/2026 adiciona três Models (PlanejamentoEvento, PropostaFornecedor e EntradaEspera) e quatro fluxos completos: comparação de propostas, conflitos da agenda, lista de espera automática e cronograma sugerido. Consulte [docs/QUATRO_RECURSOS.md](docs/QUATRO_RECURSOS.md). CRUD de propostas usa a própria Model; filtros/ranking e FIFO usam Repositories. Os Services aplicam as regras sem SQL nos Controllers.
