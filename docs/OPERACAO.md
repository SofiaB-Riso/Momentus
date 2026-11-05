# Instalação, atualização e backup

## Desenvolvimento

Requer Python 3.11 ou superior. Instale `backend/requirements.txt`, copie `.env.example` para `.env` e execute `app.py` dentro de `backend`. O servidor e o frontend usam o mesmo endereço. Nunca abra as páginas por `file://`.

Sem SECRET_KEY no desenvolvimento, a aplicação gera um segredo privado em `backend/instance/.session-secret`. Preserve-o nos backups para manter sessões; não publique seu conteúdo. Pacotes de instalação nova podem conter banco vazio. A revisão de interface preserva os arquivos de execução recebidos no ZIP do grupo e deve ser tratada como uma cópia privada da instalação.

## Atualizar uma instalação existente

1. Pare o servidor e faça backup do banco, dos uploads, do segredo e da configuração `.env`. Guarde uma cópia da versão anterior do código.
2. Extraia a nova versão em outra pasta. Preserve o seu banco ao atualizar a instalação; não o substitua pelo banco de outro pacote. Transfira seus arquivos de execução e `.env` para os caminhos correspondentes, ou mantenha DATABASE_URL e UPLOAD_FOLDER apontando para os caminhos existentes.
3. Atualize as dependências com `py -m pip install -r requirements.txt`. O banco desta revisão recebe quatro tabelas novas por `create_all()`, sem ALTER nas tabelas anteriores. O script MySQL inclui o mesmo esquema; o procedimento continua exigindo execução do SQL.
4. Inicie localmente, faça login, confira os eventos e os arquivos, as preferências e os termos. Contas antigas precisam declarar a faixa etária nas Configurações. Não há preenchimento retroativo de aceites ou autorizações.
5. Informações alimentares antigas sem classificação deixam de aparecer no painel e nos relatórios. O titular deve revisá-las pelo RSVP. Não marque em lote que dados antigos de alergia são preferências comuns.

`create_all()` não é um sistema geral de migração. Mudanças futuras em colunas exigem migrações versionadas e teste de atualização. Se precisar voltar à versão anterior, pare o servidor e restaure juntos o código, o banco e os uploads da mesma cópia. Não tente desfazer alterações apagando tabelas manualmente.

## Backup SQLite e restauração

Na pasta `backend`, com o servidor parado para manter banco e arquivos consistentes:

```powershell
py scripts/backup.py criar --saida ../backups/momentus-2026-10-30.zip
py scripts/backup.py restaurar --arquivo ../backups/momentus-2026-10-30.zip --destino ../restauracao-teste
```

O destino do backup deve ser um arquivo novo. A restauração aceita apenas pasta nova ou vazia e cria `backend/instance/momentus.db`, uploads e o segredo, quando presente na origem. Não sobrescreve uma instalação em uso. Verifica manifesto, SHA-256 e integridade SQLite; recusa caminhos externos e links simbólicos. A ferramenta limita a restauração a 2 GB descompactados.

Para outro caminho SQLite, informe `--banco` e `--uploads`. A configuração `.env` deve ter cópia separada e protegida. Para MySQL/MariaDB, use o backup próprio do servidor de banco e copie os uploads com o aplicativo parado; esta ferramenta não exporta esses bancos.

Os backups contêm dados pessoais e podem conter dados de saúde e o segredo da sessão. Mantenha-os em local restrito e protegido; o ZIP não os criptografa. Teste a restauração periodicamente e combine com o grupo o prazo de retenção. Uma cópia restaurada deve respeitar exclusões e revogações ocorridas depois do backup, antes de retornar ao uso.

## Hospedagem

Prepare `backend/.env` com:

- `APP_ENV=production`, `FLASK_DEBUG=false` e SECRET_KEY aleatória de pelo menos 32 caracteres. Exemplo de geração: `py -c "import secrets; print(secrets.token_urlsafe(48))"`.
- PUBLIC_BASE_URL com o domínio HTTPS real. Esse domínio define os Hosts aceitos; o proxy deve preservar Host.
- `PRIVACY_DEMO=false` e identificação/contatos reais de privacidade. Os contatos acadêmicos não configuram um canal de atendimento real.
- DATABASE_URL, UPLOAD_FOLDER, Google e SMTP conforme os serviços contratados. Nunca envie `.env`, chaves ou backups ao repositório.

Execute `py serve.py`, que usa Waitress. Por padrão, escuta em 127.0.0.1:5000 com 32 threads; SSE ocupa conexões duradouras, portanto monitore a capacidade antes de aumentar o público. Configure um proxy HTTPS, desative o buffer das rotas de atualizações e mantenha timeout apropriado para SSE. O servidor de desenvolvimento não deve ser publicado.

TRUST_PROXY_HEADERS só deve ser `true` quando há exatamente um proxy confiável diante do aplicativo, sem acesso direto público ao Waitress. Caso contrário, mantenha `false`. As opções de bind estão em `.env.example`. Em produção, cookies exigem HTTPS e os cabeçalhos incluem HSTS. O modo de produção recusa segredo fraco, URL sem HTTPS ou contatos de privacidade ausentes/demonstrativos.

## Proteções HTTP e limites

As chamadas que alteram dados obtêm `GET /auth/csrf` e enviam X-CSRF-Token. `frontend/js/api.js` faz isso automaticamente, inclusive em uploads. Clientes próprios precisam manter o cookie e enviar o token. Origens diferentes são recusadas; a aplicação não depende de CORS.

Sessões usam HttpOnly, SameSite=Lax e duração máxima de oito horas. Redefinir senha invalida sessões anteriores. A política de conteúdo restringe scripts ao próprio site, bloqueia enquadramento e objetos externos, preservando as fontes Google e links de mapas em outra aba. Respostas de conta e evento não ficam em cache.

Há limites por IP/conta para login, cadastro, recuperação, responsáveis e catálogo. Os contadores são protegidos entre threads de **um processo**, reiniciam com o servidor e não são distribuídos. Para vários processos/servidores, implemente um armazenamento compartilhado ou limite equivalente no proxy antes de escalar. Um bloqueio retorna HTTP 429 com Retry-After.

O fuso de eventos e lembretes é APP_TIMEZONE, padrão America/Sao_Paulo; registros de auditoria são UTC. As preferências de notificações controlam avisos internos, não envios de e-mail. Convites e autorizações são compartilhados por link privado; não são enviados automaticamente.

## Verificar dependências e código

```powershell
py -m pip install -r requirements-dev.txt
py -m unittest discover -s tests -v
py -m pip check
py -m pip_audit -r requirements.txt
py -m ruff check . --select E4,E7,E9,F,I --ignore E402
```

Use uma instalação atual do pip. Atualizações de dependências precisam de novos testes; ausência de alertas conhecidos não garante ausência de falhas. Os resultados desta entrega estão em `RESULTADO_TESTES.md` na raiz.
