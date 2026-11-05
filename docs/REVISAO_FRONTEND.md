# Revisão de interface — 05/11/2026

## Acabamento de todas as páginas

As 15 páginas usam frontend/css/acabamento.css após os estilos existentes, mantendo a identidade roxa/lilás e os destaques dourados. Tipografia, bordas, sombras, foco, formulários, espaçamento e contraste seguem uma apresentação comum. Os módulos próprios do evento e do planejamento continuam separados.

| Área | Refinamento |
|---|---|
| Login e cadastro | Campos delimitados, respiro entre blocos, botão destacado e marca do login também no celular. Termos e aceite permanecem acessíveis pela rolagem. |
| Início e eventos | Cabeçalhos, métricas, calendário, listas, cartões e estados vazios. Tamanho e animação lateral dos ingressos preservados. |
| Catálogo | Filtros, localização, cartões coloridos, avaliação, ações, favorito e carregamento adicional. Sem fotos Google; Street View mantido. |
| Configurações | Cartões de perfil/preferências, bloco de autorização com espaçamento, links de privacidade e zona de risco identificada. Ordem das duas colunas preservada. |
| Evento e planejamento | Acabamento dos controles compartilhados com os demais painéis, preservando navegação, prévia, relógio, abas, modais e permissões. |
| Recuperação/redefinição | Cartões próprios, instruções, estados de envio/erro/sucesso e ações de retorno. Duas senhas com olhinho; divergência recebe foco. Link inválido permite solicitar outro, e sucesso retira o formulário. Links reabertos na mesma aba recarregam o token em memória. |
| RSVP e colaboração | Hierarquia de título/detalhes, campos com contraste, botões, preferências/consentimentos e confirmação. RSVP sem link válido tem título, explicação e retorno. |
| Autorização de responsável | Cabeçalho de marca/retorno, campos, decisões, links de documentos e rodapé organizados. |
| Termos e privacidade | Introdução, índice por âncoras (recolhível), coluna de leitura, cartões de PDF, tabela e contato. Texto e quatro PDFs preservados. |

### Verificação e entrega

512 medições das páginas/estados em oito dimensões e dois temas, além das 176 medições da regressão de evento/planejamento. Sem excesso horizontal, IDs duplicados ou exceções JavaScript. Recuperação, troca de senha, uso único/expiração, autorização, links e PDFs exercitados; 30 fluxos principais repetidos no computador e celular. Backend: 166 testes aprovados. Resultados e limites completos em [RESULTADO_TESTES.md](../RESULTADO_TESTES.md).

O ZIP atual foi preparado com 25 tabelas vazias e sem uploads de usuários ou segredo de sessão antigo. Os dados dos testes não são entregues. As configurações e os documentos foram mantidos. Para usar essa entrega vazia, extraia em pasta nova; o aplicativo passa a persistir os novos cadastros normalmente.

## Histórico — 30/10/2026

Esta revisão usa como base o arquivo Momentus(1).zip fornecido pelo grupo. O banco, os anexos, a configuração local e os documentos desse arquivo foram preservados. Os testes usaram uma instalação separada, com dados descartáveis, Google e e-mail simulados.

## Correções

| Área | Ajuste |
|---|---|
| Cadastro | Campos organizados em duas colunas quando há espaço e uma no celular, marca visível no celular, rótulos e orientações, termos agrupados e aceite inicialmente desmarcado. |
| Cadastro e login | Altura natural da página e largura limitada ao espaço disponível. Cabeçalho, formulário, botão e rodapé deixam de ser cortados pela centralização dentro de uma altura fixa. |
| Carregamento dos termos | Nova tentativa sem recarregar a página nem perder o preenchimento. Cadastro permanece bloqueado até obter a versão. |
| Validação do cadastro | Confirmação de senha identificada, foco no campo incorreto ou na mensagem da API, estado de envio e manutenção dos dados em erros. Destino de retorno inválido usa a página inicial. |
| Páginas públicas | Termos, privacidade, recuperação e autorização de responsável deixam de herdar o espaço reservado ao menu móvel da área autenticada. |
| Início | Estatísticas adaptadas a telas estreitas, valores e textos longos contidos nos cards. O carrossel de ingressos continua com rolagem própria. |
| Notificações | Painel posicionado dentro da janela, fora do cabeçalho animado, com altura limitada e rolagem interna. Fechamento por Esc e estado expandido informado. |
| Menu | Controles do menu fechado ficam fora da navegação por teclado. Menu aberto controla o foco e fecha por Esc; mudança para a largura de computador libera novamente o conteúdo. |
| Planejamento e evento | Grades podem encolher sem ultrapassar a janela; cabeçalhos e ações quebram linha quando necessário. Participantes, colaboração, perfil e convites comportam nomes longos. |
| Modais | Controles fechados ficam ocultos e inativos; diálogos do evento têm rótulo, foco, Tab e Esc. As janelas aparecem acima do botão do menu e respeitam a altura disponível. |
| Convites de colaboração | E-mail obrigatório nos dois modos de criação; mensagem de sucesso orienta compartilhar o link, sem afirmar envio de notificação que não ocorreu. |
| Acessibilidade | Campos de busca e presença possuem nomes acessíveis; campos de autenticação no celular usam texto de 16 px para evitar zoom automático ao editar. |

## Verificações

- 15 páginas e abas do evento conferidas em 320×740, 360×800, 390×844, 768×1024, 1024×768, 1366×768, 1920×1080 e 844×390, incluindo fontes Poppins/Playfair carregadas: 176 estados de layout, sem excesso de largura da página, sobreposição entre conteúdo e rodapé, IDs duplicados ou exceções JavaScript.
- Cadastro exercitado em celular e computador: falha e nova tentativa de carregar termos, links dos documentos, checkbox obrigatório, mostrar senha, senhas diferentes, falha da API, preservação dos campos, cadastro real e redirecionamento.
- Menu, mudança de tamanho, painel com 25 notificações, relógio, catálogo 20 → 40, fechamento do modal, criação de colaborador, perfil, tema escuro, RSVP e nomes longos conferidos pela interface com backend real e dados temporários.
- 124 testes Python aprovados; os 22 scripts passaram por node --check. As 15 páginas têm IDs únicos e referências locais a scripts/estilos existentes.
- As 30 funcionalidades principais foram repetidas pela interface em 1366 px e 390 px, com verificação das chamadas de Controller/Service e persistência em SQLite temporário; sem exceções JavaScript.
- Os arquivos de execução e os quatro PDFs foram comparados byte a byte com o ZIP de origem. Caches Python e ambientes instalados não fazem parte do pacote atualizado.

## Limites

A validação de interface foi feita em Chromium com tamanhos de janela simulados; não substitui testes em aparelhos físicos com Safari/iOS e outros navegadores. O envio real de e-mail e as cotas/credenciais Google não foram exercitados. Os termos em PDF não foram reescritos. A aplicação continua sem IA e com capas coloridas no catálogo, mantendo Street View.

O pacote preserva dados e configurações da instalação recebida e deve ser mantido privado. O .gitignore exclui configuração local, segredo da sessão, banco e uploads do versionamento; a publicação do código deve respeitar essas exclusões.


## Agenda, propostas, cronograma e contraste — 03/11/2026

- A comparação exibe dia e horário do início/fim consultados; horários iguais em dias diferentes permanecem independentes. Alterar campos invalida o resultado anterior.
- Cadastrar proposta virou uma ação destacada no cabeçalho. O formulário fica aberto, sem acordeão; o botão leva até ele e posiciona o foco. Editar preserva o mesmo fluxo e o título acompanha o modo de edição.
- O cronograma se adapta ao tempo restante até a festa. Datas não caem em meses anteriores à geração quando o evento está próximo. No celular, o prazo aparece abaixo do título da tarefa, com fonte maior e sem segundos desnecessários.
- O tema escuro passa a usar um token próprio para texto de destaque, separado do roxo que serve de fundo. Isso corrige valores financeiros, preços e estados de interação. Controles nativos seguem color-scheme; ícone ativo do menu, botões, seleções, placeholders, status e gradientes recebem contraste apropriado. A identidade em lilás/rosa/coral foi mantida, com gradientes mais escuros nesse tema.
- Foram conferidos páginas públicas, telas autenticadas e abas do evento, além dos estados de relógio, notificações e escolha de evento no catálogo. Detalhes da execução estão em RESULTADO_TESTES.md.


## Cadastro e autocomplete — 04/11/2026

- Cadastro com autocomplete off no formulário e dados pessoais; new-password nas duas senhas, nomes estáveis e método POST. E-mail fica imediatamente antes das novas senhas; telefone e idade vêm depois.
- A limpeza de telefone recusa um endereço de e-mail inteiro, em vez de aproveitar seus algarismos. Eventos de entrada, mudança e foco do formulário cobrem preenchimento tardio disparado ao selecionar a senha; pageshow cobre restauração da página. Não há timers que apaguem senhas, campos fictícios ou bloqueio de colagem.
- A página de login foi mantida sem alterações. Os testes de navegador validam cadastro, confirmação da senha, olhinho, telefone opcional/com +, correção de e-mail indevido, persistência, perfil e login nas larguras de 1366, 390 e 320 px, em claro e escuro.
- O teste utiliza um perfil de Chromium descartável: não tem acesso às senhas salvas no Brave do usuário. O comportamento exato do menu de credenciais permanece sob controle do navegador. autocomplete off é uma solicitação; gerenciadores podem ignorá-la.


## Acabamento do painel do evento — 04/11/2026

- Cabeçalho com tipo traduzido para os tipos conhecidos, data/local, status, acesso e progresso circular conectado ao checklist persistido. Indicadores distinguem convites reais, presenças confirmadas, tarefas concluídas, orçamento estimado e despesas; a informação de convidados previstos continua separada da lista de convites.
- Dez seções organizadas em quatro áreas. Menu interno com ícones/contagens no desktop; seletor nativo em telas menores, com acompanhamento da rolagem. Não foram removidos recursos nem criadas categorias sem conteúdo.
- Navegação por teclado (setas, Home e End), relações tab/tabpanel, foco visível e respeito a prefers-reduced-motion. O hash da URL guarda a seção; nomes inválidos ou seções indisponíveis caem em Informações.
- Formulários, indicadores, cartões informativos, propostas e listas receberam ritmo de espaçamento, bordas e tipografia. CSS exclusivo do evento evita alterar as telas aprovadas anteriormente. Botões principais usam cores de contraste consistente em cada tema.
- O histórico permanece restrito ao dono; o modo de leitura não mostra formulários de edição. O foco/aba e os dados digitados são preservados no re-render. A montagem final da consulta inicial também preserva campos que já foram preenchidos durante o carregamento.
- Nenhuma dependência, rota, regra de negócio, Model ou tabela foi adicionada. Os novos arquivos de apresentação são evento.css e evento-interface.js.

A validação desta revisão está descrita no RESULTADO_TESTES.md. As capturas de inspeção usam dados fictícios em banco/armazenamento temporários; nenhuma conta ou evento de demonstração foi gravado no banco distribuído.

## Google Maps, rateio e catálogo — 04/11/2026

- Ações de rota no evento, nas sugestões/locais e no convite RSVP mostram somente Google Maps. Street View do catálogo foi mantido.
- O rateio explicita sua regra existente: responsável e colaboradores com convite aceito. A contagem de convidados da festa aparece separada e identificada como fora da divisão; convites pendentes não entram no cálculo.
- Atalho para convidar colaborador, disponível ao dono. Opções de cálculo com descrições, fórmula, soma das cotas planejadas e valores individuais com centavos. Quando há arredondamento, o resumo mostra a faixa de valores e explica a distribuição do centavo restante.
- A divisão automática sem despesas orienta registrar gastos em Finanças, com atalho para a seção. A cota fixa permanece independente do total de gastos. O quadro não afirma que as cotas já foram pagas.
- Salvos do catálogo deixa explícito que são estabelecimentos. O padrão de persistência zero não aparece como preço gratuito; quantidade e total zerados também ficam ocultos. Valores reais de itens antigos continuam visíveis e no cálculo financeiro. Não foram criados produtos fictícios nem uma página vazia de estoque.
- Textos novos disponíveis em português, inglês e espanhol. Layout ajustado aos temas existentes, rótulo acessível no interruptor e grupo de opções identificado.
- Alterações limitadas ao frontend e à documentação. Nenhuma mudança em regras do backend, esquema, banco, configurações, uploads ou termos em PDF.

## Atalhos de planejamento e convite de colaboração — 04/11/2026

- Card Planejar evento no Início: ação convertida para link com nome acessível, preservado ao remontar os cards. Removido o handler inline que era bloqueado pela política de segurança do servidor.
- Mesma correção nos atalhos do topo de Todos os eventos e no retorno de Planejar para a listagem. A política de segurança não foi flexibilizada.
- Menu de Todos os eventos e dos detalhes do evento: Planejar usa o ícone branco de navegação, corrigindo a variante roxa aplicada à seção inativa.
- Colaborador pendente: ações Ver convite e Copiar link visíveis ao dono, junto ao nome/e-mail. O convite pode ser aberto sem copiar manualmente uma mensagem temporária. Copiar ou visualizar não cria outro convite nem muda seu status.
- A página pública existente de colaboração foi aprimorada: data/horário, e-mail indicado, explicação da participação, cadastro/login com retorno ao convite, troca explícita de conta, aceite/recusa e acesso direto ao evento após aceitar. Estados já respondidos, link sem token, convite inválido e falha temporária têm apresentação própria.
- A simulação usa duas contas reais em uma instalação descartável, sem exigir SMTP. Nenhum aceite é automático; o backend continua validando a conta convidada. Não foi criada uma segunda página concorrente com a mesma função.
- Nenhuma rota, tabela, regra de negócio ou dependência de execução nova. Dados, configurações, anexos e PDFs preservados.

## Evento, planejamento e criação real — 05/11/2026

- Planejamento em quatro blocos, com atalhos por âncora, indicadores numerados, tipos com SVG e estado selecionado anunciado por aria-pressed. Campos de data, relógio, duração, endereço, convidados, estilo, orçamento e observações mantêm os IDs e as validações existentes. Não é necessário preencher as seções em uma sequência obrigatória.
- Prévia de nome, tipo, data, horário, convidados e orçamento; resumo com destaque próprio e sugestões para depois de salvar. CSS exclusivo da página, com cores de texto/controles adaptadas aos temas e uma coluna no celular. O módulo de prévia só acompanha os campos necessários e evita alterações no DOM quando o texto não mudou.
- Carregamento inicial representado por mensagem de status; o formulário aparece pronto para criar ou editar. A digitação e persistência das observações foram verificadas. Não há campo fictício, intervalo que apague dados ou necessidade de recriar os controles.
- Evento com calendário/contagem em dias, próxima tarefa pendente priorizando o menor prazo informado, atalhos para as seções e observações em bloco próprio. Estados sem tarefas e checklist concluído têm textos próprios. A navegação existente, leitura compartilhada, histórico restrito e atualização dos dados permanecem.
- Ingresso: criado_em vem do registro original de criação, em UTC; a data da festa deixa de ser usada como substituta. O frontend mostra agora há pouco abaixo de uma hora e tempo relativo a partir de uma hora; data exata no título e marcação time. O texto é atualizado sem remontar os cards a cada minuto e ao voltar à aba. Instantes ausentes, inválidos ou muito à frente do relógio não geram uma idade fictícia.
- Nenhuma foto, produto, IA ou dependência de execução nova. Não há migração de banco; configurações, SQLite, anexos e termos foram preservados. Consulte o README para atualizar o frontend e os dois arquivos de código do backend responsáveis pela criação real.
