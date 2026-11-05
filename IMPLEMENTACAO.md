# Mapa de implementação da disciplina

A lista oficial desta entrega é a seção **Funcionalidades Implementadas** do [README.md](README.md), com 40 casos de uso completos. A [matriz de rastreabilidade](docs/FUNCIONALIDADES.md) indica tela/controle, rota HTTP, Controller em classe, Service específico, Model e tabela de cada um.

## Arquitetura

- `backend/controllers`: classes por recurso, sem regras de negócio. `registro.py` conecta os métodos aos Blueprints e `contexto.py` fornece os casos de uso com a identidade da requisição.
- `backend/services`: uma classe por ação; validações, permissões e coordenação transacional. Os auxiliares de lembretes, notificações, cálculos e liberação também são classes.
- `backend/models`: 25 entidades em arquivos próprios, herdando de db.Model e CrudModel. A persistência básica está na Model e o caso de uso decide o momento do commit.
- `backend/repositories`: consultas especializadas, relatórios, regras de acesso a coleções e reserva atômica. O CALL de MySQL fica encapsulado em EventoRepository.
- `backend/services/integracoes`: comunicação externa com Google. A chave vem do ambiente; o provider adapta os contratos de busca/foto.
- `backend/application`: contratos, erros e composição. `backend/infrastructure`: transação, adaptadores de contratos, exportadores e arquivos locais.

O fluxo detalhado e SOLID estão em [ARQUITETURA.md](ARQUITETURA.md).

## Diagrama do domínio

Veja [docs/diagrama_classes.md](docs/diagrama_classes.md), as onze vistas em docs/diagramas e o inventário de 25 Models em docs/modelos.json. O script backend/scripts/gerar_diagrama.py regenera as fontes e o inventário sem acessar um banco.

## Demonstração e validação

O [roteiro do vídeo](docs/roteiro_video.md) prioriza os novos fluxos em uma sequência sugerida de até cinco minutos. O grupo precisa gravar/enviar o vídeo, publicar o código e conferir o acesso do professor. Os resultados executados e seus limites estão em [RESULTADO_TESTES.md](RESULTADO_TESTES.md).

A entrega atual foi preparada com um banco novo: 25 tabelas e nenhum registro, sem arquivos enviados por usuários nem o segredo antigo da sessão. As configurações e os quatro PDFs foram preservados. Os testes usam outras bases temporárias e não entram no ZIP. A aplicação não apaga dados ao iniciar; a limpeza corresponde somente ao pacote entregue.

O acabamento de todas as 15 páginas está em frontend/css/acabamento.css, após os estilos existentes. As telas públicas de senha, RSVP, autorização, termos e privacidade receberam organização própria. Os termos/privacidade têm índice de seções, preservando o texto; os PDFs permanecem idênticos. recuperacao.js cuida dos estados de envio/erro/sucesso, da confirmação da nova senha e da reabertura de links na mesma aba. senha.js é compartilhado com login/cadastro. Não há nova Model ou migração por essa revisão visual.

Em 05/11/2026, o planejamento ganhou quatro seções com prévia e navegação por âncoras, e a visão geral do evento ganhou contagem regressiva, próxima tarefa e atalhos. Os ingressos mostram o tempo real desde a criação: o Repository consulta o registro original no histórico, o Service serializa o instante UTC e o frontend apresenta o tempo decorrido. As edições preservam a criação; eventos antigos sem registro não recebem uma data fictícia. Não há nova tabela ou funcionalidade extra contabilizada por esses ajustes visuais. O README explica os arquivos de backend que precisam acompanhar a atualização do frontend.

As proteções e os fluxos adicionados na auditoria estão no README: autorizações de menores, consentimento alimentar, preferências persistidas, recuperação de comprovante, idempotência e exclusão de dados vinculados. Os identificadores 1–36 foram preservados; a extensão de 03/11 acrescenta os casos 37–40 no roteiro e na matriz; esses aprimoramentos não são contados artificialmente como novas telas independentes.


A extensão de 03/11/2026 adiciona três Models (PlanejamentoEvento, PropostaFornecedor e EntradaEspera) e quatro fluxos completos: comparação de propostas, conflitos da agenda, lista de espera automática e cronograma sugerido. Consulte [docs/QUATRO_RECURSOS.md](docs/QUATRO_RECURSOS.md). CRUD de propostas usa a própria Model; filtros/ranking e FIFO usam Repositories. Os Services aplicam as regras sem SQL nos Controllers.
