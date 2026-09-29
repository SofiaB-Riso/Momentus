# Momentus

Plataforma web para organização colaborativa de festas e eventos. Este projeto usa **Flask + SQLAlchemy** no backend e **HTML/CSS/JavaScript** no frontend.

## O que está implementado

- Cadastro e login com dois tipos de conta: **cliente** e **fornecedor/parceiro**.
- Senhas armazenadas com hash e autenticação por **sessão HttpOnly**.
- Pessoa criadora do evento gravada como **dona (`owner_id`)**.
- **Convidados** separados de **colaboradores**: um convidado não precisa ter conta e não ganha permissão de edição.
- RSVP público por link/token, com confirmação, recusa, pendência e restrições alimentares. Convidados também podem assumir itens da lista compartilhada sem criar conta nem virar colaboradores.
- Convite de colaboradores por link/token, vínculo automático quando a pessoa cria/entra na conta com o mesmo e-mail e controle de permissão de edição.
- Lista compartilhada de itens (junta-panelas), checklist, cronograma e histórico de alterações.
- Orçamento, despesas reais, teto de gastos, rateio automático/fixo e upload de comprovante (imagem/PDF).
- Calculadora de suprimentos, estimativa de orçamento base e recomendações de fornecedores/espaços.
- Catálogo ligado a contas reais de fornecedores e painel para eles criarem/alterarem/excluírem produtos e serviços.
- Integração com Google Maps por link de busca do local do evento.
- Notificações internas de RSVP, colaboração, alterações de data/horário/local, proximidade do evento e prazos de tarefas.
- Exportação de relatório do evento em **PDF e Excel**, incluindo convidados, despesas e listas de itens.
- Galeria compartilhada de fotos.
- Privacidade da lista de confirmados no RSVP.
- Favoritos gravados no banco de dados.
- Tema, idioma e preferências de interruptores são as únicas informações persistidas em `localStorage`.

## Estrutura

```text
Momentus-main/
├─ backend/
│  ├─ app.py
│  ├─ controllers/
│  ├─ models/
│  ├─ repositories/
│  ├─ services/
│  ├─ database/create_database.sql
│  └─ requirements.txt
└─ frontend/
   ├─ index.html          # login
   ├─ cadastro.html       # escolha cliente/fornecedor + cadastro
   ├─ inicio.html         # dashboard do cliente
   ├─ evento.html         # gestão completa do evento
   ├─ rsvp.html           # convite público de convidado
   ├─ convite.html        # convite de colaboração
   └─ js/, css/, assets/
```

## Como rodar com SQLite (mais simples)

No terminal, entre na pasta `backend`:

```bash
cd backend
python -m venv .venv
```

Ative o ambiente virtual no Windows:

```bash
.venv\Scripts\activate
```
Caso seja Linux ou macOS
```bash
source .venv/bin/activate
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

Copie `.env.example` para `.env`:

```bash
copy .env.example .env
```

```bash
python app.py
```

Abra no navegador:

```text
http://127.0.0.1:5000
```

> Não abra os HTMLs com duplo clique / Live Server. A autenticação usa sessão do Flask e o frontend é servido pelo próprio backend.

## Como rodar com MySQL

1. Execute `backend/database/create_database.sql` no MySQL 8+.
2. Crie `backend/.env` com, por exemplo:

```env
DATABASE_URL=mysql+pymysql://root:SUA_SENHA@localhost/momentus_db
SECRET_KEY=troque-esta-chave
FLASK_DEBUG=True
```

3. Rode `python app.py` dentro de `backend`.

## Relação principal do banco

- `usuarios` → clientes e fornecedores autenticados.
- `fornecedores` / `produtos_fornecedor` → perfil comercial e catálogo.
- `eventos.owner_id` → pessoa dona do evento.
- `convidados` → pessoas convidadas para a festa; não são usuários nem colaboradores obrigatoriamente.
- `colaboradores_evento` → pessoas que receberam permissão para ajudar na organização.
- `itens_compartilhados`, `itens_evento`, `tarefas_evento`, `despesas_evento`, `fotos_evento` → dados operacionais do evento.
- `notificacoes`, `favoritos_fornecedor`, `logs_evento` → funcionalidades auxiliares persistidas no banco.

## Diagrama de Classes

![App Screenshot]()

## Observações

- O envio do convite é feito por **link copiável**. O projeto não configura um provedor de e-mail/SMS externo.
- A integração de mapa abre o Google Maps no endereço/local pesquisado; não exige chave de API.
- Uploads são salvos em `backend/uploads/` e têm limite de 8 MB por requisição.
