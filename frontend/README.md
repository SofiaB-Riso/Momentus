# Frontend Momentus

Abra a interface pelo Flask em `http://127.0.0.1:5000`. As instruções de instalação estão no [README principal](../README.md).

## Páginas

Login e cadastro: `index.html` e `cadastro.html`. Área autenticada: `inicio.html`, `planejar.html`, `eventos.html`, `evento.html`, `catalogo.html` e `configuracoes.html`. Convites: `rsvp.html` e `convite.html`. Autorizações de responsáveis: `autorizacao.html`. Recuperação: `recuperar-senha.html` e `redefinir-senha.html`. Documentos públicos: `termos.html` e `privacidade.html`.

## JavaScript

| Arquivo | Responsabilidade |
|---|---|
| `utils.js` | Escape de texto/atributos, estrelas e datas; carregado antes dos consumidores. |
| `api.js` | Requisições HTTP, token CSRF, sessão e tratamento das respostas do backend. |
| `app.js` | Sessão, cache em memória, traduções, tema e operações da conta/eventos. |
| `script.js` | Menu, Início, calendário, planejamento, perfil e notificações. |
| `auth.js` | Formulários de login e cadastro. |
| `eventos.js` | Busca e ações da lista de eventos. |
| `evento.js` / `evento-planejamento.js` | Gestão do evento, colaboração, arquivos, descoberta e histórico. |
| `horario.js` | Relógio de 24 horas e foco/cancelamento do diálogo. |
| `localizacao-momentus.js` | Localização e controles compartilhados entre as páginas de fornecedores. |
| `catalogo-google.js` / `inicio-fornecedores.js` | Catálogo paginado e lista compacta do Início. |
| `rsvp.js` / `convite.js` | Convites públicos e colaboração por token. |
| `autorizacao.js` / `autorizacao-conta.js` | Decisão do responsável e controles de autorização nas Configurações. |
| `tema-inicial.js` / `senha.js` | Tema antes da renderização e controles de mostrar senha. |

`css/style.css` usa variáveis de tema e componentes compartilhados. Os ícones ficam em `assets/icones`, incluindo as variantes de item ativo. As capas do catálogo usam gradientes; a Galeria do evento continua permitindo uploads dos participantes.

A sessão vem do cookie HttpOnly do Flask; perfil e eventos não são guardados no localStorage. Tema, idioma e cache de localização são preferências do navegador. As preferências de notificações são persistidas por conta no backend. SSE atualiza o painel/RSVP preservando campos em edição. Os cálculos financeiros são feitos no backend. Formulários bloqueiam envios repetidos; despesas também enviam uma chave de idempotência.

As regras de filtros, lotes de vinte, rascunhos e localização estão descritas no README principal, evitando instruções duplicadas entre arquivos.

## Fluxos da disciplina

A página individual consulta explicitamente GET /eventos/<id> e mantém o cache sincronizado com a resposta autorizada. As tarefas possuem botões independentes para conclusão e exclusão; quando não há registros, a lista fica vazia com uma mensagem, sem tarefas fictícias. O preenchimento em andamento continua preservado nas atualizações automáticas.

Os 36 casos demonstráveis e seus controles estão em [docs/FUNCIONALIDADES.md](../docs/FUNCIONALIDADES.md). A interface continua usando capas coloridas no catálogo, Street View, lotes de vinte, rascunhos, relógio e a animação lateral dos ingressos. Português é o idioma completo; inglês/espanhol cobrem navegação e componentes compartilhados, com esse alcance informado nas Configurações.

## Responsividade e acesso aos formulários

`cadastro.html` mantém todos os IDs do fluxo de conta e agrupa os documentos em um fieldset próprio. O formulário usa duas colunas quando há espaço e uma no celular, com rolagem da página, sem altura fixa que corte os controles. O script `auth.js` permite repetir o carregamento dos termos e mantém os dados preenchidos em falhas da API.

O menu móvel usa inert quando fechado e controla o foco enquanto aberto. As notificações são posicionadas em relação à janela, fora do cabeçalho animado, com altura limitada e rolagem interna. Os modais do evento ocultam seus controles quando fechados e permitem navegação por Tab e fechamento por Esc. As páginas públicas usam a classe bodyPaginaLegal para não receber o espaçamento do menu da área autenticada. Veja [a validação desta revisão](../docs/REVISAO_FRONTEND.md).
