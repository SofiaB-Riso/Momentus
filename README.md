# Momentus

Aplicação de planejamento de eventos em Python/Flask e SQLAlchemy, com interface em HTML, CSS e JavaScript. O Flask serve as páginas e a API no mesmo endereço.

## Funcionalidades

- Cadastro, login, perfil e exclusão de conta. Uma única conta pode criar eventos e aceitar convites de colaboração.
- Criação e edição de eventos, tipos personalizados pela opção Outro, orçamento digitável e horário HH:MM com seletor de relógio.
- Início com todos os eventos acessíveis em ordem de data/horário, rolagem horizontal e Planejar evento no final. Ingressos com animação lateral e respeito à preferência de movimento reduzido.
- Rascunhos editáveis, separados dos eventos ativos, das estatísticas e do calendário. Todos os eventos também estão disponíveis pelo menu lateral.
- Convidados, RSVP público, restrições alimentares, privacidade, colaboração com permissões e histórico de alterações.
- Itens compartilhados com reserva atômica, itens do catálogo, tarefas com prazo e progresso, despesas, comprovantes, rateio e galeria do evento.
- Resumo com estimativas de orçamento/suprimentos, busca de espaços, recomendações, notificações, lembretes e relatórios PDF/Excel.
- Catálogo com capas coloridas, favoritos, Maps e Street View. Melhores avaliados exige nota **maior que 4** e **mais de 200 avaliações**. A carga inicial e cada clique em Carregar mais acrescentam até vinte locais únicos, enquanto houver resultados.
- Temas claro/escuro, traduções pt/en/es e layout responsivo.

## Executar no Windows

Com Python instalado, abra o terminal na pasta do projeto:

```powershell
cd backend
py -m pip install -r requirements.txt
Copy-Item .env.example .env
py app.py
```

Se quiser isolar as dependências, crie e ative um ambiente virtual antes da instalação. O ZIP não inclui venv nem dependências instaladas.

No Linux/macOS, use `python3` em vez de `py` e `cp .env.example .env` para copiar a configuração.

Acesse **http://127.0.0.1:5000**. Abra pelo Flask: os arquivos HTML precisam da API e dos cookies de sessão desse servidor.

## Configuração

Ajuste `backend/.env` a partir de `.env.example`:

| Variável | Uso |
|---|---|
| `DATABASE_URL` | Padrão SQLite: `sqlite:///momentus.db`. Também aceita MySQL/MariaDB pelo driver PyMySQL. |
| `SECRET_KEY` | Chave usada para assinar as sessões; defina sua própria chave antes de compartilhar a aplicação. |
| `GOOGLE_MAPS_API_KEY` | Chave do Google para as buscas externas; mantida no backend. |
| `UPLOAD_FOLDER` | Diretório opcional de uploads; padrão `backend/uploads`. |
| `FLASK_DEBUG` | Modo de desenvolvimento. |

Para usar MySQL, execute `backend/database/create_database.sql`, configure `DATABASE_URL=mysql+pymysql://USUARIO:SENHA@localhost/momentus_db` e inicie o Flask. O SQL cria o esquema e o procedimento `sp_eventos_por_tipo`; `create_all()` não cria procedimentos nem migra tabelas existentes.

### Banco vazio e pasta instance

O projeto usa **um único SQLite padrão em `backend/instance/momentus.db`**, independentemente de como o módulo Flask é iniciado. A pasta `instance` duplicada da raiz foi retirada.

O banco entregue mantém as 16 tabelas e **zero registros**, sem contas ou dados de demonstração. Para começar do zero, pare o servidor anterior e extraia em uma pasta nova e vazia; depois faça um novo cadastro. Bancos externos indicados por `DATABASE_URL` continuam pertencendo à instalação que os configurou.

`instance` guarda dados locais de execução. Após usar o sistema, seu banco conterá os cadastros e eventos; removê-lo apaga esses dados. Os uploads de usuários ficam em `backend/uploads`, não em `frontend/assets`.

### Google e localização

Configure Places API (New) para as buscas externas. Os cards não solicitam fotos do Google; usam gradientes. Street View depende das coordenadas e da cobertura do serviço. Links de Maps e Waze do evento usam o endereço informado.

Com GPS, a busca considera a localização e ordena os locais por distância em linha reta, sem corte de distância; resultados sem coordenadas ficam no final. Melhores avaliados prioriza nota e quantidade de avaliações. O campo manual aceita bairro e cidade, sem inventar distâncias. O cache de coordenadas expira em dez minutos e o de cidade em seis horas. O botão de localização solicita uma posição nova.

A paginação guarda candidatos excedentes e consulta páginas adicionais quando necessário para completar vinte novos resultados únicos. Se a fonte acabar, mostra o restante. Falhas permitem tentar novamente, preservando os cards existentes. A quantidade disponível depende do Google, do filtro e das cotas da conta.

## Organização

| Diretório/arquivo | Responsabilidade |
|---|---|
| `backend/controllers` | HTTP, autenticação da requisição e SSE. `contexto.py` constrói os casos de uso. |
| `backend/services` | Casos de uso, regras de acesso e coordenação das operações. |
| `backend/models` / `repositories` | Entidades, CRUD, consultas especializadas e reservas atômicas. |
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

Os convites são compartilhados por link copiável; não há serviço externo de envio de e-mail/SMS configurado. O limite de upload é de 8 MB por requisição. Preferências de interface e localização podem ficar no navegador; os dados de eventos e de conta ficam no servidor.
