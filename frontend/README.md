# Frontend Momentus

Abra a interface pelo Flask em `http://127.0.0.1:5000`. As instruções de instalação estão no [README principal](../README.md).

## Páginas

Login e cadastro: `index.html` e `cadastro.html`. Área autenticada: `inicio.html`, `planejar.html`, `eventos.html`, `evento.html`, `catalogo.html` e `configuracoes.html`. Convites: `rsvp.html` e `convite.html`.

## JavaScript

| Arquivo | Responsabilidade |
|---|---|
| `utils.js` | Escape de texto/atributos, estrelas e datas; carregado antes dos consumidores. |
| `api.js` | Requisições HTTP e tratamento das respostas do backend. |
| `app.js` | Sessão, cache em memória, traduções, tema e operações da conta/eventos. |
| `script.js` | Menu, Início, calendário, planejamento, perfil e notificações. |
| `auth.js` | Formulários de login e cadastro. |
| `eventos.js` | Busca e ações da lista de eventos. |
| `evento.js` / `evento-planejamento.js` | Gestão do evento, colaboração, arquivos, descoberta e histórico. |
| `horario.js` | Relógio de 24 horas e foco/cancelamento do diálogo. |
| `localizacao-momentus.js` | Localização e controles compartilhados entre as páginas de fornecedores. |
| `catalogo-google.js` / `inicio-fornecedores.js` | Catálogo paginado e lista compacta do Início. |
| `rsvp.js` / `convite.js` | Convites públicos e colaboração por token. |

`css/style.css` usa variáveis de tema e componentes compartilhados. Os ícones ficam em `assets/icones`, incluindo as variantes de item ativo. As capas do catálogo usam gradientes; a Galeria do evento continua permitindo uploads dos participantes.

A sessão vem do cookie HttpOnly do Flask; perfil e eventos não são guardados no localStorage. Tema, idioma, interruptores e cache de localização são preferências do navegador. SSE atualiza o painel/RSVP preservando campos em edição. Os cálculos financeiros são feitos no backend.

As regras de filtros, lotes de vinte, rascunhos e localização estão descritas no README principal, evitando instruções duplicadas entre arquivos.
