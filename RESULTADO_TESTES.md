# Validação — Momentus

## Refinamento completo e entrega vazia — 05/11/2026

Esta é a validação do ZIP atual. As seções seguintes registram revisões anteriores; a decisão atual do grupo é receber o banco vazio.

| Verificação | Resultado |
|---|---|
| Backend | **166 testes aprovados** com unittest, Flask e SQLite temporário. |
| Fluxos completos | **30 casos principais pela interface em 1366 e 390 px**, com chamadas HTTP reais, Controller/Service observados e persistência conferida. Incluem cadastro/login, perfil, eventos, convidados/RSVP, colaboração/permissões, itens, tarefas, despesas/comprovantes, rateio, galeria e relatórios PDF/Excel. |
| Revisão de todas as páginas | **512 medições de layout** em oito dimensões e dois temas: 15 páginas, estados vazios, abas do evento, links inválidos e estados de sucesso. Sem excesso horizontal ou IDs duplicados. Capturas conferidas em celular/computador. |
| Planejamento e evento | Regressão adicional em quatro combinações de largura/tema: criar, editar, tipo personalizado, relógio, orçamento com centavos, observações persistidas, prévia, rascunho, idade real do ingresso e atalhos. **176 medições adicionais** de planejamento/abas. |
| Senhas e autorização | Recuperação com mensagem genérica, senhas divergentes, mostrar/ocultar senha, redefinição real, limpeza do formulário no sucesso, senha antiga recusada e nova aceita, link reutilizado/expirado recusado, link reaberto na mesma aba, token removido do endereço e autorização real de responsável em conta temporária. |
| Fontes e documentos | **15 HTMLs e 25 JavaScripts** conferidos; node --check aprovado, referências locais existentes, sem handlers inline. Os textos normativos de termos/privacidade e os **quatro PDFs** são idênticos à origem. PDFs disponíveis por HTTP com tipo application/pdf. |
| Inspeção Python | Ruff E4/E7/E9/F aprovado, com exceção pontual E402 para scripts/gerar_diagrama.py: esse utilitário ajusta sys.path antes de importar as Models. Nenhum código Python da aplicação foi alterado por esta revisão visual. |
| Banco do pacote | Banco SQLite recriado com as Models atuais: **25 tabelas, zero registros**, integrity_check ok e foreign_key_check sem inconsistências. Sem arquivos de usuários nem segredo de sessão anterior. Configuração .env preservada byte a byte. |
| Primeira execução | Cópia descartável inicia sem sessão/contas/eventos, serve as 15 páginas e permite criar a primeira conta com ID 1. Reiniciar preserva esse cadastro; não existe reset automático. O banco do ZIP permanece vazio após todos os testes. |

Dimensões da revisão completa: 320×740, 360×800, 390×844, 768×1024, 1024×768, 1366×950, 1920×1080 e 844×390, em claro/escuro. A regressão adicional usa 1366×768 no lugar de 1366×950. Zero exceções JavaScript nas execuções aprovadas.

O navegador utilizado foi Chromium com dimensões simuladas. Não houve teste em aparelhos físicos ou envio real de e-mail. Google e entrega de e-mail foram simulados nos testes; cotas, credenciais externas e SMTP real não foram consumidos. O código dos testes de interface, as capturas e as bases temporárias não integram o ZIP.

## Evento, planejamento e tempo real de criação — 05/11/2026

Revisão de apresentação e do campo criado_em do DTO. A API obtém o primeiro registro evento_criado em uma agregação do Repository, junto da revisão. Não há alteração de Model, tabela, migração, configuração ou arquivo de usuário.

- **166 testes Python aprovados**, incluindo três regressões novas: criação presente na listagem/detalhe e estável após editar; leitura do instante UTC original; ausência de registro histórico sem invenção de data. Os 163 testes anteriores também passaram.
- **25 scripts JavaScript** com sintaxe validada. Todas as páginas HTML conferidas para IDs únicos, referências locais de scripts/estilos e ausência de handlers inline.
- **Quatro fluxos completos no navegador**, em 1366 e 390 px, nos temas claro e escuro: criar tipo personalizado, escolher horário no relógio, duração, orçamento livre com centavos, digitar e persistir observações, conferir a prévia, salvar, editar com preenchimento preservado, salvar/retomar rascunho e abrir o evento pela animação do ingresso.
- **Tempo de criação**: ingresso recém-criado; horário do histórico ajustado somente no banco descartável para dez horas antes; exibição Criado há 10 horas e título com data exata; versão em inglês; edição sem reiniciar a contagem. Verificação isolada dos limiares de uma hora, 24 horas, mês e ano, idioma espanhol e dados ausentes/inválidos/futuros. A atualização periódica foi exercitada com relógio simulado no navegador, mantendo a mesma instância DOM do ingresso.
- **176 medições de layout**: planejamento e as dez seções do evento em oito dimensões, nos dois temas. Sem excesso de largura da página ou IDs duplicados. Dimensões: 320×740, 360×800, 390×844, 768×1024, 1024×768, 1366×768, 1920×1080 e 844×390. Telas conferidas visualmente no computador/celular, incluindo os dois temas.
- **30 casos principais repetidos pela interface em 1366 e 390 px**, com API Flask real, Controller/Service observados e persistência SQLite conferida. Inclui autenticação, perfil, criação/edição/exclusão de evento, convidados/RSVP, colaboração/permissões, lista compartilhada, tarefas, despesas/comprovantes, rateio, galeria e relatórios PDF/Excel. O novo destaque de próxima tarefa foi conferido nos estados de checklist completo e vazio; os atalhos da visão geral foram executados. Zero exceções JavaScript nos fluxos desta revisão.
- Ruff E4/E7/E9/F aprovado no backend. Os três arquivos Python alterados também passaram na organização de imports I. A base anterior já apresentava avisos I001 em outros arquivos; esta revisão não reorganizou os imports de todo o projeto.

Os testes usaram Chromium, fontes em cache, Flask e SQLite/uploads temporários, com integrações externas simuladas. Nenhum cadastro de demonstração foi incluído no banco do pacote e nenhuma cota real de Google ou SMTP foi consumida. As capturas são de inspeção interna. Configurações, SQLite, uploads e termos em PDF permanecem idênticos à versão anterior. Para atualizar uma instalação existente, o README lista o frontend e os dois arquivos de código do backend necessários ao horário real.

## Atalhos e convite de colaboração — 04/11/2026

Correções exclusivamente no frontend e na documentação. A política de segurança, as rotas, os casos de uso, as tabelas e os arquivos de backend foram preservados.

- **163 testes Python aprovados**, repetidos com bancos temporários nesta revisão; **24 scripts JavaScript** aprovados em node --check. Todas as páginas HTML passaram pela conferência de IDs únicos, referências locais a scripts/estilos e ausência de handlers inline.
- **Quatro fluxos completos no navegador**: 1366 e 390 px, nos temas claro e escuro. Card Planejar no Início exercitado com zero e três eventos, inclusive após remontar os cards; navegação para Planejar pelo topo de Todos os eventos e retorno para a listagem. A resposta do Flask manteve script-src 'self'; nenhuma violação de CSP foi registrada nesses fluxos.
- Ícone de Planejar: variante branca conferida no menu de Todos os eventos; aplicada também aos detalhes do evento. A variante ativa permanece exclusiva da própria página Planejar.
- Convite criado pelo painel, visualizado em nova aba e copiado sem duplicação. Abertura com outra conta não altera a participação. Cadastro pela página pública retornou ao convite; aceite habilitou o evento na conta convidada, atualizou a lista do responsável e passou o rateio para duas pessoas. Recusa persistiu após recarregar. Login, logout explícito/troca de conta e retorno ao convite também foram executados pela interface.
- Estados sem token, token inválido e falha temporária com nova tentativa exercitados. Convite já respondido não mostra novamente ações de aceite/recusa. Zero exceções JavaScript nos quatro fluxos.
- **32 medições de layout** na lista de colaboradores e no convite com outra conta: oito dimensões nos dois temas, sem excesso de largura da página ou IDs duplicados. Dimensões: 320×740, 360×800, 390×844, 768×1024, 1024×768, 1366×768, 1920×1080 e 844×390. Páginas públicas de convite/aceite e listas conferidas visualmente em computador/celular.
- **Duas verificações adicionais após o aceite**, em 1366 e 390 px: reabrir o convite, alterar o e-mail da conta e continuar acessando o evento; outra conta e visitante não recebem acesso pelo token, enquanto login com a conta vinculada retorna ao convite aceito. A permissão é confirmada pela API do evento.

Os testes usaram Flask real com SQLite e uploads temporários, Google/e-mail simulados e fontes em cache. Não foram enviadas mensagens reais, consumidas cotas Google ou criadas contas de teste no banco do pacote. A distribuição mantém os arquivos de backend, configurações, banco, anexos e PDFs idênticos à versão anterior. Não há dependência ou migração nova. O passo a passo para testar com duas contas está no README.

## Google Maps, rateio e estabelecimentos salvos — 04/11/2026

Alterações no frontend e na documentação, preservando backend, regras de cálculo, banco, configurações, uploads e PDFs.

- **163 testes Python aprovados**, repetidos nesta revisão com bancos temporários.
- **24 scripts JavaScript** aprovados em node --check.
- Fluxos reais de navegador em **1366 e 390 px, nos temas claro e escuro**: rateio automático sem despesas, atalho para Finanças, cota fixa com uma pessoa, convite pelo atalho, exclusão de pendentes, aceite com outra conta, entrada de dois colaboradores, R$ 100 divididos em R$ 33,34/R$ 33,33/R$ 33,33, remoção de participante, retirada de despesa e desativação do rateio.
- Permissão de leitura conferida: rateio visível com controles desabilitados e sem ação de convidar. Contagem de dois convidados da festa separada dos participantes da divisão. Textos novos exercitados também em inglês e espanhol.
- Catálogo com Google simulado: vinte resultados, adição pela interface, persistência/recarregamento do estabelecimento sem preço, sem quantidade e sem total zerado; despesa existente permanece inalterada. Item antigo com preço informado de R$ 12,35 × 3 mantém exibição e total de R$ 37,05; a remoção restaura a lista sem total artificial.
- Google Maps como única opção de rota no evento, nas sugestões de fornecedores e no convite RSVP; nenhuma opção visível de Waze nesses fluxos. Street View do catálogo não foi alterado.
- **48 medições de layout**: Colaboração, Salvos do catálogo e Informações em oito dimensões, nos dois temas, sem alargamento da página ou IDs duplicados. Dimensões: 320×740, 360×800, 390×844, 768×1024, 1024×768, 1366×768, 1920×1080 e 844×390. Conferência visual adicional dos estados de rateio e catálogo em computador/celular, nos dois temas. Zero exceções JavaScript nos quatro fluxos completos.

O navegador usou Flask real, SQLite/uploads descartáveis e integrações externas simuladas. Não consumiu a cota real do Google nem gravou contas de teste no banco entregue. A conferência de preservação do pacote compara os arquivos com a versão anterior; nenhum arquivo de backend foi alterado. Não há migração ou dependência nova.

## Refinamento visual do evento — 04/11/2026

Revisão de frontend com CSS e módulo de apresentação próprios do evento. O backend, banco, configurações, anexos e PDFs foram preservados. Os 163 testes Python registrados abaixo pertencem à validação anterior; não foram repetidos nesta alteração exclusivamente de interface.

- Navegação e layout: as dez seções em oito dimensões, nos dois temas (160 medições), sem alargamento da página ou IDs duplicados. Foram verificados seleção, recarga por hash, navegação de teclado e preservação de formulário/foco durante atualização dos dados.
- Regressão: os 30 casos principais foram executados novamente pela interface em 1366 e 390 px, com API, Controller, Service e persistência SQLite conferidos.
- Recursos recentes: propostas, conflitos, fila/promoção no RSVP e cronograma foram exercitados novamente pela interface nas duas larguras.
- Acesso: leitura e edição compartilhada, histórico restrito, foco após atualização e evento removido verificados no desktop/celular.
- Contraste: inspeção automatizada auxiliar e conferência visual dos temas; a medição não é certificação formal de acessibilidade.
- Código: 24 scripts JavaScript conferidos com node --check. Não há nova dependência de execução.

Os testes usaram Chromium e um backend real com SQLite/uploads temporários, com integrações externas simuladas. Nenhum dado dos testes foi incluído no banco do pacote.


## Revisão de cadastro — 04/11/2026

Esta revisão altera somente cadastro, limpeza de telefone e documentação. Backend, banco, configurações e PDFs foram preservados. A suíte Python de 163 testes abaixo pertence à validação de 03/11; não foi repetida por esta alteração de frontend.

**Seis cenários de navegador aprovados, sem exceções JavaScript:** cadastro e telefone nas larguras de 1366, 390 e 320 px, em claro/escuro; confirmação divergente com correção, mostrar/ocultar senha, telefone opcional vazio/com +, descarte de e-mail inserido indevidamente, persistência via API, atualização do perfil, logout e login. A página de login permanece byte a byte igual à versão anterior.

O perfil de teste é descartável, sem as credenciais reais do usuário. A validação confere o pedido de autocomplete e os fluxos; não garante a supressão do menu do gerenciador de senhas do Brave.

## Validação anterior — 03/11/2026

Revisão aplicada ao ZIP atualizado fornecido pelo grupo, mantendo a versão sem IA e os cards do catálogo sem fotos Google. Os testes rodaram com SQLite, uploads temporários e provedores externos simulados; não usaram as credenciais ou os dados reais do projeto.

## Resultados desta entrega

| Verificação | Resultado |
|---|---|
| Suíte Python/Flask/SQLAlchemy | **163 testes aprovados**: os 153 da entrega anterior e dez regressões novas de datas/cronograma. Controllers em classes, Services, persistência, permissões, validações, concorrência, uploads, consentimentos, CSRF, recuperação e backup. |
| Comparação de propostas | Total com Decimal, taxas/descontos, divisão de centavos, filtro de categoria, serviços necessários, teto, ranking, ausência de destaque sem opção adequada, edição/exclusão e isolamento entre eventos/contas. |
| Conflitos de agenda | Sobreposição, horários adjacentes sem conflito, virada da meia-noite, exclusão do próprio evento/rascunhos/cancelados, privacidade de outras contas, duração válida e persistida, horários iguais em datas diferentes e virada de dia somente na data correta. |
| Lista de espera | FIFO, reenvio sem perder posição, saída/reentrada ao final, desistência/exclusão com promoção, ampliar/desativar capacidade, recusa de limite abaixo dos confirmados, painel respeitando vagas, confirmação simultânea sem exceder limite, posição privada no RSVP, autorização de menor e liberação de itens. |
| Cronograma | Seis etapas persistidas; reutilização do checklist; geração idempotente; recálculo conforme data/tipo; preservação de concluídas e tarefas manuais; exclusão em cascata das novas entidades. A revisão verifica compressão das etapas no período disponível, seis tipos de festa, véspera, horas restantes do mesmo dia, evento passado, mudança isolada do horário, ausência de horário e preservação de concluídas/manuais ao encurtar a data. |
| Quatro novos fluxos no navegador | Executados pela interface em **1366 px e 390 px**, com backend real: comparação e persistência das propostas, conflito no planejamento, uma vaga/dois convites e promoção após desistência, geração/conclusão/recálculo de tarefas. Zero exceções JavaScript. |
| Regressão anterior de navegador | A versão base já tinha os 30 casos principais validados nas duas larguras, com requisições, Controller/Service e registros SQLite conferidos. Nesta revisão, a suíte Python completa foi repetida e o navegador concentrou-se nos quatro recursos, nos dois temas, na responsividade e nos estados interativos afetados. |
| Responsividade | **368 medições nos temas claro/escuro, em oito dimensões**: 320×740, 360×800, 390×844, 768×1024, 1024×768, 1366×768, 1920×1080 e 844×390. Inclui 15 páginas e painéis do evento; sem alargamento da página, sobreposição do rodapé, IDs duplicados ou exceções JavaScript. Novas telas conferidas visualmente. O fluxo de criação de proposta fica aberto e tem ação de destaque. Prazos no celular usam fonte maior e data/hora sem segundos. |
| Contraste e interação | Inspeção de 24 páginas/painéis com medição auxiliar de contraste de texto; estados de relógio, notificações, escolha de evento no catálogo e campos financeiros/propostas conferidos em claro/escuro, nas larguras de 1366 e 390 px. A medição é apoio técnico e não uma certificação formal de acessibilidade. |
| Código | Ruff E4/E7/E9/F/I aprovado (E402 ignorado para inicialização dos testes). Todos os scripts JavaScript conferidos com node --check. Nenhuma nova dependência de execução. |
| Arquitetura e documentação | Matriz com 40 casos totais; inventário das **25 Models** coerente com os metadados; **11 vistas UML** Mermaid/SVG, incluindo propostas e planejamento/fila. Os novos fluxos estão documentados sem contabilizar suas operações auxiliares como funcionalidades extras. |
| Preservação | Os oito arquivos originais de configuração, banco, avatar e PDFs foram comparados byte a byte com o ZIP recebido e preservados. Uma cópia descartável do banco foi atualizada de 22 para 25 tabelas: todos os registros anteriores permaneceram iguais, integrity_check e foreign_key_check aprovados. O banco distribuído permanece o original; as três novas tabelas são criadas na inicialização. |

## Reproduzir

Na pasta backend, com Python 3.11 ou superior:

```powershell
py -m pip install -r requirements-dev.txt
py -m unittest discover -s tests -v
py -m ruff check . --select E4,E7,E9,F --ignore E402
```

Os 39 testes dos quatro recursos e suas correções estão em tests/test_quatro_recursos.py. A suíte usa bancos temporários e não envia mensagens reais. A verificação de navegador desta revisão usou Chromium, fontes em cache e serviços externos simulados em servidor descartável, fora do código distribuído.

Para conferir os fluxos manualmente, siga [docs/QUATRO_RECURSOS.md](docs/QUATRO_RECURSOS.md). A descrição das correções anteriores de cadastro/layout permanece em [docs/REVISAO_FRONTEND.md](docs/REVISAO_FRONTEND.md).

## Limites da validação

- Os novos recursos funcionam localmente sem chave adicional. Propostas são orçamentos informados pelo usuário; conflitos consultam apenas eventos acessíveis, sem verificar a disponibilidade pública do estabelecimento. Cronogramas são sugestões comprimidas ao período disponível; tarefas manuais/concluídas mantêm seus prazos originais. Um cronograma gerado pela versão anterior precisa ser regerado para corrigir suas etapas automáticas pendentes.
- A lista de espera usa avisos no convite e notificações internas; não envia e-mail nem faz reserva em serviços externos.
- SMTP real, cotas/conta Google e hospedagem não foram exercitados. Recuperação de senha e catálogo mantêm as configurações necessárias já documentadas no README.
- Não foi usado servidor MySQL/MariaDB. O SQL inclui as 25 tabelas; persistência, atualização do banco e concorrência foram verificadas com SQLite. Orientações de produção/backup: [docs/OPERACAO.md](docs/OPERACAO.md).
- A identificação de responsável continua declaratória, conforme o sistema anterior. Os PDFs fornecidos não foram alterados. A validação é técnica, sem certificação jurídica.
- Não foram realizados commit/push nem gravação/publicação do vídeo. O grupo deve demonstrar e enviar os resultados pelo canal da disciplina. A classificação acadêmica das funcionalidades depende do professor.
