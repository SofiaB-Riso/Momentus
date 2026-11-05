# Momentus

Aplicação de planejamento de eventos em Python/Flask e SQLAlchemy, com interface em HTML, CSS e JavaScript. O Flask serve as páginas e a API no mesmo endereço.

## Entrega limpa e refinamento de todas as páginas — 05/11/2026

Este ZIP contém o banco SQLite com as **25 tabelas vazias**, sem conta, evento, convite, token, foto ou comprovante de usuário. Não existe conta padrão. O segredo da sessão da instalação anterior também foi retirado; o aplicativo gera um novo na primeira execução.

**Extraia o ZIP em uma pasta nova** e inicie o Flask conforme as instruções abaixo. Crie sua própria conta em **Crie sua conta**. O aplicativo salvará normalmente os novos cadastros e eventos: a limpeza foi feita somente para preparar esta entrega, sem reset automático ao iniciar. As configurações locais e os quatro PDFs foram mantidos.

As 15 páginas receberam acabamento de tipografia, espaçamento, formulários, cartões, botões, foco e contraste, com ajustes para celular e computador. Isso inclui Início, Todos os eventos, Catálogo, Configurações, planejamento, as abas do evento, login, cadastro, RSVP, colaboração, autorização de responsável, recuperação/redefinição de senha, termos e privacidade. Os documentos têm índice por seções; os textos aprovados e os PDFs continuam iguais.

O acabamento compartilhado fica em `frontend/css/acabamento.css`, carregado após os estilos existentes. A recuperação de senha mostra estados de envio, erro e sucesso; a redefinição permite mostrar/ocultar as duas senhas, trata senhas diferentes e oferece ações para entrar ou solicitar outro link. O envio de e-mail continua dependendo da configuração SMTP. Veja os resultados em [RESULTADO_TESTES.md](RESULTADO_TESTES.md).

## Funcionalidades Implementadas

Cada item abaixo é um caso de uso disponível na interface e ligado à API Flask, a uma Controller em classe, a um Service próprio e às Models/Repositories do banco. A matriz [docs/FUNCIONALIDADES.md](docs/FUNCIONALIDADES.md) registra a tela, o controle, a rota, as classes e a tabela de cada fluxo.

1. Cadastrar conta.
2. Entrar na conta.
3. Atualizar perfil.
4. Excluir a própria conta.
5. Criar evento.
6. Listar eventos acessíveis.
7. Consultar os detalhes de um evento.
8. Atualizar um evento.
9. Excluir um evento.
10. Cadastrar convidado.
11. Atualizar a presença de convidado pelo painel.
12. Remover convidado.
13. Responder RSVP e informar restrições alimentares.
14. Convidar colaborador.
15. Aceitar ou recusar convite de colaboração.
16. Atualizar a permissão de um colaborador.
17. Remover colaborador.
18. Adicionar item à lista compartilhada.
19. Atribuir ou liberar o responsável por um item.
20. Remover item compartilhado.
21. Criar tarefa com prazo.
22. Concluir ou reabrir uma tarefa.
23. Remover tarefa.
24. Registrar despesa.
25. Anexar comprovante a uma despesa.
26. Excluir despesa.
27. Configurar o rateio das despesas.
28. Enviar foto para a galeria do evento.
29. Remover foto da galeria.
30. Gerar relatório do evento em PDF ou Excel.
31. Enviar ou substituir foto de perfil.
32. Remover foto de perfil.
33. Solicitar recuperação de senha.
34. Redefinir senha por link de uso único.
35. Registrar aceite dos termos.
36. Exportar dados da própria conta em JSON.
37. Comparar propostas de fornecedores por custo e serviços.
38. Verificar conflitos de horário na agenda.
39. Gerenciar vagas e promover automaticamente a lista de espera.
40. Gerar e recalcular o cronograma do evento.

Os relatórios consultam dados persistidos; uploads gravam seus metadados no banco e os arquivos no armazenamento configurado. O catálogo externo, os mapas, as estimativas, os favoritos, o histórico, os lembretes e os temas continuam disponíveis como recursos complementares.

## Diagrama de classes

O [diagrama do domínio](docs/diagrama_classes.md) apresenta as 25 Models, seus principais atributos, cardinalidades, herança, composição e agregação em onze vistas legíveis. Inclui SVGs e fontes Mermaid em [docs/diagramas](docs/diagramas), além do [inventário gerado das Models](docs/modelos.json).

## Executar no Windows

Com **Python 3.11 ou superior** instalado, abra o terminal na pasta do projeto:

```powershell
cd backend
py -m pip install -r requirements.txt
if (!(Test-Path .env)) { Copy-Item .env.example .env }
py app.py
```

Se quiser isolar as dependências, crie e ative um ambiente virtual antes da instalação. O ZIP não inclui venv nem dependências instaladas.

No Linux/macOS, use `python3` em vez de `py`. Se ainda não existir `.env`, copie `.env.example` para esse nome; mantenha a configuração quando ela já estiver presente.

Acesse **http://127.0.0.1:5000**. Abra pelo Flask: os arquivos HTML precisam da API e dos cookies de sessão desse servidor.

## Configuração

Ajuste `backend/.env` a partir de `.env.example`:

| Variável | Uso |
|---|---|
| `DATABASE_URL` | Padrão SQLite: `sqlite:///momentus.db`. Também aceita MySQL/MariaDB pelo driver PyMySQL. |
| `SECRET_KEY` | Chave aleatória de pelo menos 32 caracteres em produção. No desenvolvimento, um segredo por instalação é gerado em `backend/instance/.session-secret`. |
| `GOOGLE_MAPS_API_KEY` | Chave do Google para as buscas externas; mantida no backend. |
| `UPLOAD_FOLDER` | Diretório opcional de uploads; padrão `backend/uploads`. |
| `APP_ENV` / `FLASK_DEBUG` | `development` ou `production`; debug desligado por padrão e sempre desligado em produção. |
| `APP_TIMEZONE` | Fuso das datas locais de eventos e lembretes; padrão `America/Sao_Paulo`. |
| `PUBLIC_BASE_URL` | Endereço do site usado nos links de recuperação; HTTPS obrigatório em produção. |
| `PRIVACY_DEMO` | `true` usa os contatos acadêmicos do grupo no desenvolvimento; produção exige `false` e contatos configurados. |

Para usar MySQL, execute `backend/database/create_database.sql`, configure `DATABASE_URL=mysql+pymysql://USUARIO:SENHA@localhost/momentus_db` e inicie o Flask. O SQL cria o esquema e o procedimento `sp_eventos_por_tipo`; `create_all()` não cria procedimentos nem migra tabelas existentes.

### Banco local e pasta instance

O projeto usa **um único SQLite padrão em `backend/instance/momentus.db`**, independentemente de como o módulo Flask é iniciado. A pasta `instance` duplicada da raiz foi retirada.

O esquema tem 25 tabelas. A entrega atual inclui todas elas vazias, a pedido do grupo. Os uploads da instalação anterior foram retirados do pacote. `create_all()` prepara tabelas ausentes e não apaga registros nas próximas execuções. Para atualizar outra instalação preservando seus dados, siga [atualização e backup](docs/OPERACAO.md). Bancos externos indicados por `DATABASE_URL` continuam pertencendo à instalação que os configurou.

`instance` guarda dados locais de execução. Após usar o sistema, seu banco conterá os cadastros e eventos; removê-lo apaga esses dados. Os uploads de usuários ficam em `backend/uploads`, não em `frontend/assets`.

### Google e localização

Configure Places API (New) para as buscas externas. Os cards não solicitam fotos do Google; usam gradientes. Street View depende das coordenadas e da cobertura do serviço. O evento, o convite RSVP e as sugestões de locais oferecem somente Google Maps, usando o endereço informado.

Com GPS, a busca considera a localização e ordena os locais por distância em linha reta, sem corte de distância; resultados sem coordenadas ficam no final. Melhores avaliados prioriza nota e quantidade de avaliações. O campo manual aceita bairro e cidade, sem inventar distâncias. O cache de coordenadas expira em dez minutos e o de cidade em seis horas. O botão de localização solicita uma posição nova.

A paginação guarda candidatos excedentes e consulta páginas adicionais quando necessário para completar vinte novos resultados únicos. Se a fonte acabar, mostra o restante. Falhas permitem tentar novamente, preservando os cards existentes. A quantidade disponível depende do Google, do filtro e das cotas da conta.

### Estabelecimentos salvos e rateio

Em **Salvos do catálogo**, ficam os estabelecimentos adicionados ao evento. A integração atual do Google Places fornece informações do local, sem uma lista de produtos com seus preços. Por isso, os locais salvos aparecem sem preço, quantidade ou total zerado. Consulte os valores com o fornecedor; registre propostas no comparador e gastos efetivos em Finanças. Salvar um estabelecimento não registra uma despesa. Itens antigos que tenham preço real informado continuam exibindo seu valor e integrando o cálculo financeiro existente.

O **rateio**, na seção Colaboração, inclui o responsável pelo evento e os colaboradores ativos que aceitaram o convite. Convidados da festa e convites de colaboração pendentes ficam fora. Use **Convidar colaborador para dividir** e compartilhe o link para que a pessoa aceite com sua conta.

- **Dividir as despesas:** divide o total financeiro pelos participantes do rateio. Exemplo: R$ 300 entre o responsável e dois colaboradores ativos resulta em R$ 100 para cada um. Centavos restantes são distribuídos para a soma fechar exatamente.
- **Valor fixo por pessoa:** define uma cota para cada participante. R$ 150 por pessoa, com três participantes, significa R$ 450 em cotas planejadas, independentemente das despesas.

A tela informa quem entra na divisão, a fórmula utilizada, as cotas individuais e o total planejado. Não há cobrança ou confirmação de pagamento nesse quadro. Nenhuma tabela ou configuração nova é necessária nesta revisão.

### Convite de colaboração — teste local

A página pública de colaboração é `convite.html#token=...`. Ela apresenta o evento, a data, o horário e o e-mail convidado, com ações para aceitar ou recusar. O aceite usa a API real e fica salvo no banco; não depende de envio de e-mail.

1. Abra um evento, vá a **Colaboração** e escolha **Adicionar colaborador**. Informe o e-mail da pessoa e crie o convite.
2. Na linha do colaborador pendente, use **Ver convite** para abrir a página ou **Copiar link** para compartilhar. Abrir o convite não altera a participação.
3. Para simular duas pessoas no mesmo computador, abra o link em uma janela anônima. Entre ou crie uma conta com o e-mail informado no convite; o sistema retorna à página de resposta. Se estiver usando outra conta, a tela oferece **Entrar com outra conta**.
4. Aceite ou recuse. O responsável acompanha o status na lista de colaboradores. Após aceitar, **Abrir evento** leva diretamente ao planejamento e o colaborador ativo entra no rateio.

Links sem token, inválidos ou indisponíveis exibem uma orientação; falhas temporárias permitem tentar novamente. A página mantém a verificação do e-mail pelo backend.

Os atalhos de criação no card do Início e no topo de Todos os eventos, assim como o retorno de Planejar para Todos os eventos, usam links HTML. Isso mantém a navegação compatível com a política de segurança `script-src 'self'` do Flask. O ícone de Planejar no menu de Todos os eventos e nos detalhes do evento usa a variante branca das demais páginas.

## Refinamento de evento e planejamento — 05/11/2026

O planejamento está organizado em quatro blocos, com navegação por âncoras, tipos de evento com ícones vetoriais, prévia de nome/data/horário/convidados/orçamento e sugestões para depois de criar. As regras de criação, edição, rascunho, horário e comparação de agenda foram mantidas. O formulário aparece após a preparação dos dados, com indicação de carregamento, evitando edições antes de concluir o preenchimento inicial. O campo de observações foi conferido com digitação nativa e persistência.

O painel do evento recebeu um calendário com contagem em dias, a próxima tarefa pendente com prazo, atalhos para convidados/checklist/colaboração/Finanças/galeria e um bloco de observações. Esses destaques usam os dados do evento; não geram tarefas ou despesas fictícias.

O ingresso do Início mostra a criação real: abaixo de uma hora, Criado agora há pouco; a partir de uma hora, Criado há 1 hora, Criado há 10 horas, dias, meses ou anos. A data exata fica no título do elemento time. O texto se atualiza a cada minuto enquanto a página está visível e ao voltar à aba. Editar não reinicia a contagem. A API envia criado_em em UTC com Z, obtido do primeiro registro evento_criado no histórico. Eventos antigos sem esse registro deixam de exibir uma idade inventada. Não há nova coluna, tabela ou migração.

Para aplicar esta revisão a uma instalação existente, faça backup e copie a pasta frontend e os arquivos abaixo, preservando backend/instance, backend/uploads, .env e o segredo da sessão da sua instalação:

- `backend/repositories/consulta_evento_repository.py`
- `backend/services/serializacao_evento.py`
- `backend/tests/test_regressao.py` (novos testes de criação real)

Atualize também README.md, ARQUITETURA.md, IMPLEMENTACAO.md, RESULTADO_TESTES.md e docs/REVISAO_FRONTEND.md. Copiar somente o frontend não inclui o horário real na resposta da API. Essas instruções descrevem uma atualização que preserva os dados de outra instalação. Para começar sem dados com o ZIP atual, use a pasta nova descrita no início deste README. A integração de produtos ficou para uma etapa posterior.

## Organização

| Diretório/arquivo | Responsabilidade |
|---|---|
| `backend/controllers` | Classes de Controllers por recurso, transporte HTTP/SSE e adaptação da requisição. `registro.py` registra suas ações nos Blueprints e `contexto.py` constrói os casos de uso. |
| `backend/services` | Casos de uso, regras de acesso e coordenação das operações. |
| `backend/models` / `repositories` | Uma Model por entidade, CRUD herdado de CrudModel, consultas especializadas e reservas atômicas. |
| `backend/application` / `infrastructure` | Contratos, composição, transações e integrações externas. |
| `frontend/js/utils.js` | Formatação e escape de HTML compartilhados. |
| `frontend/js/localizacao-momentus.js` | Cache, GPS e controles de localização usados pelo Início e Catálogo. |
| `frontend/assets/icones` | Uma cópia de cada variante visual dos ícones do menu. |
| `backend/tests` | Testes automatizados com dados temporários. |

Veja [ARQUITETURA.md](ARQUITETURA.md) para as camadas e SOLID, [IMPLEMENTACAO.md](IMPLEMENTACAO.md) para o mapa dos requisitos e [RESULTADO_TESTES.md](RESULTADO_TESTES.md) para a validação desta revisão.

## Testes e operação

Na pasta `backend`:

```powershell
py -m unittest discover -s tests -v
py -m pip check
```

Os testes usam bancos temporários e Google simulado. Não preenchem o banco entregue. Para gerar lembretes internos, execute `py -m flask --app app gerar-lembretes`.

Para servir fora do desenvolvimento, use `py serve.py` com HTTPS em um proxy configurado e `APP_ENV=production`. A configuração, as proteções HTTP, o backup e a atualização de instalações anteriores estão em [docs/OPERACAO.md](docs/OPERACAO.md). Não use o servidor de desenvolvimento como hospedagem pública.

Os convites são compartilhados por link privado copiável. O aceite de colaboração exige a conta correspondente **e o link**; cadastrar um e-mail não concede acesso. A recuperação de senha pode enviar e-mail pelo SMTP configurado; sem SMTP a tela informa que o serviço ainda precisa ser configurado. Convites não são enviados automaticamente por e-mail ou SMS. O limite de upload é de 8 MB por requisição. Tema, idioma e localização podem ficar no navegador; preferências de notificações, eventos e conta ficam no servidor.

## Entrega da disciplina

- Demonstração: [roteiro de até cinco minutos](docs/roteiro_video.md), com os fluxos identificados pelos mesmos números do README.
- Arquitetura: [ARQUITETURA.md](ARQUITETURA.md), [matriz dos fluxos](docs/FUNCIONALIDADES.md) e diagrama do domínio.
- Verificação: [RESULTADO_TESTES.md](RESULTADO_TESTES.md) contém resultados e limites da validação desta revisão.
- O grupo deve conferir o commit/push na conta oficial e o acesso do professor, e gravar/enviar o vídeo obrigatório. A existência do roteiro não substitui o vídeo.
- A identificação de quais funcionalidades são novas em relação ao checkpoint anterior deve usar o histórico real do grupo. Esta entrega não atribui datas fictícias de implementação aos casos já existentes.

## Privacidade, autorizações e integridade — revisão de 30/10/2026

- **Cadastro:** checkbox obrigatório de leitura e aceite, desmarcado por padrão. A API valida o aceite booleano e a versão; versão e data UTC são persistidas. Contas antigas registram o próprio aceite em Configurações, sem aceite inventado retroativamente.
- **Entrar → Esqueci minha senha:** solicita recuperação por e-mail. O link abre a página de nova senha, expira em 30 minutos, tem uso único e não revela o token em respostas de API. O banco armazena apenas o hash. Novo pedido substitui links anteriores; há até três envios por conta a cada 15 minutos. Redefinir invalida sessões antigas.
- **Configurações → foto do perfil:** o botão de lápis abre a seleção; é possível substituir ou remover a foto. PNG/JPEG/WebP são reencodados em WebP, sem nome original ou metadados EXIF, em até 512×512. A foto aparece no perfil e no avatar do menu da própria conta.
- **Configurações → Privacidade e seus dados:** abaixo do perfil na coluna esquerda, oferece consulta de aceite, registro para contas antigas, download JSON e desativação da localização salva. Notificações, preferências e Zona de risco ficam na coluna direita; em telas menores, as colunas se organizam em sequência. O JSON contém conta, aceite, favoritos e informações básicas dos eventos criados. Exclui anexos, senhas, tokens e cadastros de terceiros.
- **Rodapé de todas as páginas:** Termos de Uso e Privacidade. A página de privacidade descreve os dados e finalidades, inclusive telefone, galeria/legendas, comprovantes e restrições alimentares, e apresenta o contato configurado. Os modelos PDF originais da professora estão preservados em frontend/documentos e acessíveis pelos Termos.
- **Uploads:** exigem sessão e acesso ao evento; foto de perfil só é lida pelo dono. Respostas privadas não ficam em cache. Excluir a conta remove também avatar, registro de aceite e tokens.
- **Idade e responsável:** cadastro exige declaração de faixa etária. Contas de menores aguardam autorização pelo link privado, de uso único e validade de sete dias. Configurações oferece gerar/copiar o link e revogar o acesso. Contas antigas precisam declarar a idade antes de usar os eventos. A identificação do responsável é declaratória, sem verificação documental externa.
- **RSVP e alimentação:** preferências comuns exigem confirmação de que não contêm saúde. Alergias e intolerâncias têm autorização específica do adulto ou do responsável por menor, com versão e data, independente da presença. O RSVP permite revogar e apagar essas informações. O painel não permite ao organizador registrar saúde em nome de terceiros. Dados antigos sem classificação deixam de aparecer até serem revisados pelo titular. A autorização de participação de um menor é separada da autorização opcional de saúde.
- **Despesas:** o formulário bloqueia cliques repetidos e usa uma chave de envio para não duplicar a mesma operação. Se o comprovante falhar, a despesa continua identificada como salva e a lista permite anexar novamente sem criar outra. Referências arbitrárias a arquivos são recusadas; exclusões verificam vínculo, prefixo e referências existentes.
- **Notificações e tarefas:** os dois interruptores funcionam por conta e persistem no banco. Rascunhos, eventos cancelados e concluídos não geram lembretes; adicionar uma tarefa recalcula o progresso. A opção de promoções sem implementação foi retirada.
- **Exclusão da conta:** remove dados próprios e anonimiza identificação vinculada de colaboração, histórico e pagador nos eventos de terceiros. Texto livre e cópias já exportadas podem precisar de atendimento pelo responsável, descrito em [docs/PRIVACIDADE_OPERACAO.md](docs/PRIVACIDADE_OPERACAO.md).

### Configuração de e-mail e identificação

No backend/.env, preencha PUBLIC_BASE_URL (domínio público HTTPS, ou http://127.0.0.1:5000 para uso local), SMTP_HOST, SMTP_PORT, SMTP_FROM, SMTP_USERNAME e SMTP_PASSWORD. Porta 587 usa STARTTLS; porta 465 requer SMTP_SSL=true. Nunca publique o .env. SMTP_FROM deve ser um remetente autorizado pelo provedor. O link usa PUBLIC_BASE_URL, sem confiar no cabeçalho Host da requisição. Um link local só funciona no mesmo computador que executa o servidor.

Para exibir identificação e contato reais, preencha PRIVACY_CONTROLLER, PRIVACY_OFFICER, PRIVACY_EMAIL e PRIVACY_PHONE. No desenvolvimento, os contatos acadêmicos aprovados pelo grupo são exibidos com aviso de demonstração: Sofia Braga Riso, Sofie Cirino e Castro, momentus@momentus.com e +55 31 99999-9999. Esses valores não configuram uma caixa de e-mail. Produção recusa contatos ausentes ou o modo demonstrativo. O registro de aceite do site não preenche nem substitui os campos de assinatura dos documentos acadêmicos.

Em relação à versão anterior, o aplicativo cria quatro tabelas de apoio: autorizacoes_conta, consentimentos_alimentares, preferencias_usuarios e requisicoes_despesa. Não altera colunas das 18 tabelas anteriores nem apaga seus registros. O banco incluído no ZIP está vazio. Faça backup antes de atualizar uma instalação existente. O SQL de instalação MySQL também inclui as tabelas novas; esta revisão foi validada com SQLite.

A recuperação está implementada e foi testada com SMTP simulado. O envio real depende da configuração e das credenciais do grupo, que não foram fornecidas. Não há IA nesta versão, e o catálogo mantém as capas coloridas.

### Ícone da aba do navegador

Todas as páginas usam apenas a ampulheta da marca Momentus como favicon. O SVG em frontend/assets/favicon.svg reutiliza o símbolo original; frontend/favicon.ico oferece compatibilidade em 16, 32 e 48 pixels. A versão na URL evita reutilizar o ícone anterior do cache.

### Termos preenchidos em PDF

Os PDFs revisados e fornecidos pelo grupo em 30/10/2026 estão integrados ao site em frontend/documentos/termo-uso-momentus.pdf e frontend/documentos/termo-consentimento-momentus.pdf. Os arquivos foram incluídos exatamente como recebidos, com nove páginas cada, preservando os textos, as marcações e os campos de assinatura e data. O ano dos campos de data é 2026; não há uma data de assinatura fixa para todos os usuários.

Os PDFs podem ser abertos no cadastro, em Configurações → Privacidade e seus dados e em Termos de Uso → Documentos em PDF (página acessível pelo rodapé). Esta última página oferece também os botões para baixar. Os modelos acadêmicos originais continuam preservados em arquivos separados.

Para substituir os documentos, troque os dois PDFs mantendo esses caminhos. Se o conteúdo dos termos mudar, atualize também VERSAO_TERMOS em backend/services/conta/termos.py e o texto inicial data-versao-termos em frontend/termos.html. A versão atual é 2026-10-30; os registros de aceite anteriores não são reescritos, e a tela de Configurações permite ao usuário registrar o aceite da nova versão.

Os PDFs são documentos para leitura; seus campos não são preenchidos automaticamente pelo site. O aceite geral e as autorizações específicas de saúde e responsáveis são registros separados no banco. Nenhum desses registros representa assinatura dos campos do PDF.

### Mostrar senha e menu lateral

O login e os campos de senha/confirmação do cadastro possuem botões de olho independentes para mostrar ou ocultar o valor. O controle compartilhado está em frontend/js/senha.js, usa botões que não enviam o formulário e pode ser acionado pelo teclado.

O menu lateral fica fixo à altura da tela; Sair da conta fica no rodapé, sobre o degradê ao final do menu. Em janelas baixas, a lista de opções tem rolagem própria para manter a saída acessível. No celular, o menu continua sendo aberto pelo botão de menu. O calendário do Início também permite quebrar a linha do cabeçalho em telas estreitas.

O telefone do cadastro e das Configurações aceita somente números e um sinal + opcional no início, para o código do país. Espaços, letras e pontuação são removidos ao digitar ou colar; números já salvos com formatação aparecem sem a máscara no formulário. O telefone continua opcional, e a API valida o mesmo formato ao cadastrar ou atualizar a conta.

### Idiomas

Português é o idioma completo desta versão. Inglês e espanhol traduzem a navegação e componentes compartilhados; formulários específicos e documentos acadêmicos permanecem em português. A opção na interface informa esse alcance.

### Revisão de interface — 30/10/2026

O cadastro foi reorganizado com campos em duas colunas quando há espaço, coluna única no celular e um bloco próprio para os termos. A página cresce com o conteúdo, mantendo cabeçalho, aceite, botão e rodapé acessíveis por rolagem, inclusive em janelas baixas. Falhas no carregamento dos termos permitem tentar novamente preservando o preenchimento; erros de senha e da API ficam identificados e recebem foco.

A revisão também corrige larguras no planejamento, estatísticas, participantes e convites com nomes longos. As notificações têm rolagem dentro da janela; menu e modais possuem tratamento de teclado, fechamento por Esc e foco. As páginas públicas não herdam o espaço reservado ao menu lateral. Resultados e limites estão em [docs/REVISAO_FRONTEND.md](docs/REVISAO_FRONTEND.md).


### Quatro novos fluxos — 03/11/2026

- **Evento → Comparar propostas:** registre orçamentos reais, descontos, taxas, parcelas e serviços inclusos. Compare na mesma categoria com teto e serviços necessários. O destaque considera o menor total entre as opções adequadas; não contrata nem consulta preços do Google.
- **Planejar evento → Verificar conflitos na minha agenda:** informe data, hora e duração em minutos. O sistema consulta os eventos aos quais sua conta tem acesso, identifica sobreposições (inclusive na virada do dia) e sinaliza o mesmo endereço/cidade. O aviso não verifica a agenda pública do estabelecimento nem impede salvar.
- **Evento → Convidados → Vagas e lista de espera:** ative um limite de confirmações. Novos interessados entram em ordem de solicitação quando as vagas acabam. Uma desistência/exclusão libera a vaga para a primeira pessoa elegível; o convite mostra posição e confirmação. Aumentar/remover o limite também processa a fila. Sem limite, permanece o comportamento anterior. O número estimado de convidados no planejamento é independente desse limite.
- **Evento → Tarefas → Cronograma sugerido:** gere seis etapas com prazos conforme tipo/data, reaproveitando o checklist existente. Alterar data, horário ou tipo recalcula apenas tarefas automáticas pendentes; tarefas concluídas e manuais são preservadas. Quando o tempo é curto, distribui as etapas no período entre agora e o evento, sem criar prazos passados. Para atualizar um cronograma gerado pela versão anterior, use Regerar cronograma.

Regras, limites e roteiro de conferência estão em [docs/QUATRO_RECURSOS.md](docs/QUATRO_RECURSOS.md). Os novos fluxos funcionam localmente, sem chave de API adicional.


### Ajustes de agenda, propostas e modo escuro — 03/11/2026

A consulta de conflitos mostra explicitamente a data e o horário comparados, incluindo o término no dia seguinte quando necessário. No comparador de propostas, Cadastrar proposta está destacado e o formulário fica visível. O cronograma comprime as antecedências conforme os dias disponíveis; no mesmo dia, usa as horas restantes. Novos prazos não antecedem a geração; tarefas concluídas/manuais são preservadas. O modo escuro ajusta valores, campos nativos, ícones, seleções, placeholders e gradientes para manter a leitura das informações.


### Cadastro e preenchimento do navegador — 04/11/2026

O cadastro solicita autocomplete desativado para nome, e-mail e telefone. As duas senhas são identificadas como novas, e os campos de acesso aparecem antes do telefone para reduzir a identificação incorreta dele como usuário. Um e-mail inserido no telefone é descartado, inclusive quando o gerenciador dispara a atualização ao interagir com outro campo. Valores válidos continuam aceitando dígitos e + no início.

O formulário de login permanece com seu preenchimento de credenciais existente. Senhas oferecidas pelo navegador vêm do gerenciador local e podem continuar aparecendo conforme suas configurações, mesmo sem conta no banco: o site não pode apagar essas credenciais nem garantir a supressão do menu. Para remover entradas antigas de desenvolvimento, procure localhost/127.0.0.1 no gerenciador de senhas do navegador. Sugestão de senha forte no cadastro também é uma função do navegador, não uma conta previamente criada no Momentus.

Se você já alterou ou resetou o banco no computador, aplique esta revisão copiando apenas a pasta frontend; assim, seu banco/configurações locais não são substituídos pelos do pacote.


### Página do evento — acabamento visual de 04/11/2026

A página do evento tem um cabeçalho com progresso circular do checklist e indicadores de presenças, tarefas, orçamento e despesas reais. As seções são organizadas em Visão geral, Planejamento, Orçamento e Memórias. No computador, o menu lateral interno traz ícones e contagens; em telas menores, um seletor acessível dá acesso às mesmas seções e acompanha a rolagem.

A seção selecionada permanece no endereço (por exemplo, evento.html?id=1#tarefas), permitindo recarregar e compartilhar o acesso àquela área. Permissões continuam sendo aplicadas: histórico apenas para o dono; formulários e ações conforme o acesso. Atualizações automáticas preservam o formulário em preenchimento e o foco, inclusive na carga inicial. Teclado, foco visível e redução de movimento são respeitados. Formulários, listas, cartões de propostas e informações receberam espaçamento, contraste e hierarquia próprios da página, nos dois temas.

As mudanças visuais estão em frontend/css/evento.css e frontend/js/evento-interface.js, com integração em evento.html/evento.js. Não há dependências novas, alteração do backend ou migração de banco. Para atualizar uma instalação sem substituir seus dados/configurações, copie somente a pasta frontend deste pacote.
