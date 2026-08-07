# 🎉 Momentus

> Sistema desenvolvido para auxiliar na organização de pequenos eventos de forma simples, prática e intuitiva.

---

# 👥 Integrantes

- Ana Clara Cardoso Vieira
- Cícero Lucas Moreira de Paula
- Lorenzo Nunes Saiani
- Luiza Rocha Nunes Roque
- Sofia Braga Riso
- Sofie Cirino e Castro

---

# 📖 Sobre o Projeto

O **Momentus** é uma aplicação web desenvolvida com **Flask** (Python) que permite cadastrar e gerenciar pequenos eventos.

O sistema foi criado com o objetivo de facilitar o planejamento de eventos, reunindo as principais informações em um único lugar. O back-end expõe uma **API REST**, consumida por um front-end simples em HTML, CSS e JavaScript.

---

# ✅ Funcionalidades — CRUD básico (Model)

- Cadastro de eventos
- Listagem de eventos
- Busca de evento por ID
- Edição de eventos
- Exclusão de eventos

---

# ⚙️ Funcionalidade além do CRUD básico (nesta etapa)

## Busca de eventos por tipo, com ordenação

Consulta que filtra os eventos por `tipo_evento` (`WHERE`) e devolve o resultado ordenado por nome (`ORDER BY`), implementada como **procedure no banco de dados** e chamada a partir da camada Repository — conforme a arquitetura da disciplina.

**Fluxo:**

```
Controller (evento_controller.py)
  -> Service (BuscarEventosPorTipoService)
    -> Repository (EventoRepository.buscar_por_tipo_evento)
      -> Procedure sp_eventos_por_tipo (MySQL)
```

**Rota:** `GET /eventos/por-tipo?tipo_evento=Casamento`

> ⚠️ **Observação sobre o banco:** a procedure (`sp_eventos_por_tipo`) só existe no script do MySQL (`backend/database/create_database.sql`). Quando a aplicação roda com a configuração padrão (SQLite, usada para facilitar testes em sala), o Repository usa uma consulta SQLAlchemy equivalente como *fallback*, já que SQLite não suporta procedures. **Para demonstrar a procedure de fato, é necessário rodar com MySQL** (veja a seção "Como Executar").

> ⚠️ **Pendência conhecida:** o front-end ainda **não chama** a rota `/eventos/por-tipo` — a busca exibida em `eventos.html`/`eventos.js` hoje filtra os eventos no próprio navegador (client-side), e não via API. Falta adicionar um método `buscarPorTipo` em `frontend/js/api.js` e usar a rota nova em alguma tela (ex.: um filtro por tipo de evento na listagem), para atender à exigência de que as telas usem as funcionalidades implementadas chamando as rotas corretas da API.

---

# 🗄️ Procedures Criadas

| Procedure | Banco | Descrição |
|---|---|---|
| `sp_eventos_por_tipo(IN e_tipo VARCHAR(100))` | MySQL | Retorna os eventos cujo `tipo_evento` seja igual a `e_tipo`, ordenados por `nome_evento` (`SELECT ... WHERE tipo_evento = e_tipo ORDER BY nome_evento`). Definida em `backend/database/create_database.sql`. |

---

# 🌐 Rotas da API

| Método | Rota | Função | Tipo |
|---------|------|--------|------|
| GET | / | Mensagem de status da API e lista de rotas disponíveis | — |
| GET | /eventos | Lista todos os eventos | CRUD básico |
| GET | /eventos/{id} | Exibe um evento específico | CRUD básico |
| POST | /eventos | Cadastra um novo evento | CRUD básico |
| PUT | /eventos/{id} | Atualiza um evento existente | CRUD básico |
| DELETE | /eventos/{id} | Remove um evento | CRUD básico |
| GET | /eventos/por-tipo?tipo_evento=Casamento | Lista eventos filtrados por tipo, ordenados por nome (via procedure) | Além do CRUD |

---

# 📦 Models e Repositories Utilizados

## Models

- **`Evento`** (`backend/models/evento_model.py`) — representa a entidade de domínio e concentra o CRUD básico (`salvar`, `atualizar`, `deletar`, `listar_todos`, `buscar_por_id`).

## Repositories

- **`EventoRepository`** (`backend/repositories/evento_repository.py`) — encapsula o acesso mais complexo ao banco: chama a procedure `sp_eventos_por_tipo` no MySQL (ou a consulta equivalente via SQLAlchemy, no fallback com SQLite) para a busca de eventos por tipo.

---

# 🏗️ Arquitetura

O projeto foi desenvolvido utilizando uma arquitetura em camadas, separando responsabilidades entre:

- **Models** — definição das entidades e regras de acesso ao banco (SQLAlchemy), incluindo o CRUD básico
- **Repositories** — consultas mais específicas ao banco de dados, encapsulando o uso de procedures
- **Services** — regras de negócio e validações, separados por caso de uso
- **Controllers** — recebem as requisições HTTP e retornam as respostas (Blueprints do Flask)

---

# 🛠️ Tecnologias Utilizadas

## Back-end

- Python
- Flask
- Flask-SQLAlchemy
- Flask-CORS
- python-dotenv

## Front-end

- HTML5
- CSS3
- JavaScript

## Banco de Dados

- SQLite (padrão, para facilitar os testes em sala — **não executa a procedure**)
- MySQL (necessário para rodar a procedure `sp_eventos_por_tipo`, via PyMySQL)

---

# 📂 Estrutura do Projeto

```text
Momentus/
│
├── backend/
│   ├── controllers/
│   │   └── evento_controller.py
│   ├── models/
│   │   ├── database.py
│   │   └── evento_model.py
│   ├── repositories/
│   │   └── evento_repository.py
│   ├── services/
│   │   ├── criar_evento_service.py
│   │   ├── listar_evento_service.py
│   │   ├── buscar_evento_por_id_service.py
│   │   ├── buscar_evento_por_tipo_service.py
│   │   ├── atualizar_evento_service.py
│   │   └── deletar_evento_service.py
│   ├── database/
│   │   └── create_database.sql
│   ├── app.py
│   ├── requirements.txt
│   └── .env.example
│
├── frontend/
│   ├── assets/
│   ├── css/
│   ├── js/
│   ├── catalogo.html
│   ├── configuracoes.html
│   ├── evento.html
│   ├── eventos.html
│   ├── inicio.html
│   └── planejar.html
│
└── README.md
```

---

# ▶️ Como Executar

## Pré-requisitos

- Python 3.10 ou superior
- pip
- MySQL (opcional, mas obrigatório para testar a procedure `sp_eventos_por_tipo`)

## Instalação

```bash
git clone https://github.com/SofiaB-Riso/Momentus/

cd Momentus/backend

# cria e ativa o ambiente virtual
python -m venv .venv
.venv\Scripts\activate      # Windows
source .venv/bin/activate   # Linux/Mac

# instala as dependências
pip install -r requirements.txt

# copia o arquivo de variáveis de ambiente
cp .env.example .env

# roda a aplicação
python app.py
```

A API estará disponível em:

```
http://localhost:5000
```

Para usar a interface web, abra os arquivos de `frontend/` (ex.: `inicio.html`) no navegador com a API rodando.

## Executando com MySQL (para testar a procedure)

1. Rode o script `backend/database/create_database.sql` no seu servidor MySQL — ele cria o banco `evento_db`, a tabela `eventos` e a procedure `sp_eventos_por_tipo`.
2. No arquivo `.env`, troque a `DATABASE_URL` para:
   ```
   DATABASE_URL=mysql+pymysql://root:sua_senha@localhost:3306/evento_db
   ```
3. Rode `python app.py` normalmente. A partir daí, `GET /eventos/por-tipo?tipo_evento=...` passa a chamar `CALL sp_eventos_por_tipo(...)` de fato.

---

# 📝 Status desta etapa / Pendências

- [x] Funcionalidade além do CRUD implementada no Repository (`sp_eventos_por_tipo`, com `WHERE` + `ORDER BY`)
- [x] Controller e Service dedicados para a nova funcionalidade
- [ ] Tela do front-end consumindo a rota `GET /eventos/por-tipo` (hoje a busca na tela de eventos é feita apenas no navegador, sem chamar a API)
- [ ] Confirmar com o enunciado da etapa se mais alguma funcionalidade além do CRUD é exigida (o material do Classroom fala em "funcionalidades", no plural)

---

# 🎯 Objetivo

Desenvolver uma aplicação capaz de facilitar o gerenciamento de pequenos eventos por meio das operações de cadastro, edição, visualização e exclusão de eventos, além de consultas mais elaboradas ao banco de dados.

---

# 📄 Licença

Projeto desenvolvido para fins acadêmicos.
