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

# ✅ Funcionalidades Implementadas

- Cadastro de eventos
- Listagem de eventos
- Busca de evento por ID
- Busca de eventos por tipo
- Edição de eventos
- Exclusão de eventos

---

# 📦 Model Implementada

- Evento

---

# 🌐 Rotas da API

| Método | Rota | Função |
|---------|------|--------|
| GET | / | Mensagem de status da API e lista de rotas disponíveis |
| GET | /eventos | Lista todos os eventos |
| GET | /eventos/por-tipo?tipo_evento=Casamento | Lista eventos filtrados por tipo |
| GET | /eventos/{id} | Exibe um evento específico |
| POST | /eventos | Cadastra um novo evento |
| PUT | /eventos/{id} | Atualiza um evento existente |
| DELETE | /eventos/{id} | Remove um evento |

---

# 🏗️ Arquitetura

O projeto foi desenvolvido utilizando uma arquitetura em camadas, separando responsabilidades entre:

- **Models** — definição das entidades e regras de acesso ao banco (SQLAlchemy)
- **Repositories** — consultas mais específicas ao banco de dados
- **Services** — regras de negócio e validações
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

- SQLite (padrão, para facilitar os testes em sala)
- MySQL (opcional, via PyMySQL)

---

# 📂 Estrutura do Projeto

```text
Momentus Flask/
│
├── backend/
│   ├── controllers/
│   ├── models/
│   ├── repositories/
│   ├── services/
│   ├── database/
│   │   └── create_database.sql
│   ├── app.py
│   ├── requirements.txt
│   └── .env.example
│
├── frontend/
│   ├── css/
│   ├── js/
│   └── index.html
│
└── README.md
```

---

# ▶️ Como Executar

## Pré-requisitos

- Python 3.10 ou superior
- pip

## Instalação

```bash
git clone <url-do-repositório>

cd "Momentus Flask/backend"

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

> Por padrão, o projeto usa **SQLite** e cria o banco automaticamente ao iniciar. Para usar MySQL, crie o banco com `backend/database/create_database.sql` e ajuste a `DATABASE_URL` no `.env`.

Para usar a interface web, basta abrir o arquivo `frontend/index.html` no navegador com a API rodando.

---

# 🎯 Objetivo

Desenvolver uma aplicação capaz de facilitar o gerenciamento de pequenos eventos por meio das operações de cadastro, edição, visualização e exclusão de eventos.

---

# 📄 Licença

Projeto desenvolvido para fins acadêmicos.
