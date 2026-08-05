# Backend - API Flask + SQLAlchemy

API de exemplo para demonstrar CRUD usando Flask, SQLAlchemy, Controllers, Services e Models.

## Como executar

Entre na pasta do backend:

```bash
cd backend
```

Crie e ative o ambiente virtual:

```bash
python -m venv .venv
```

No Windows:

```bash
.venv\Scripts\activate
```

No Linux ou macOS:

```bash
source .venv/bin/activate
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

Crie o arquivo `.env` com base no exemplo:

```bash
cp .env.example .env
```

Execute a API:

```bash
python app.py
```

A API ficará disponível em:

```text
http://127.0.0.1:5000
```

## Banco de dados

Por padrão, o projeto usa SQLite para facilitar o teste local:

```text
DATABASE_URL=sqlite:///evento.db
```

Para usar MySQL, execute o script:

```text
backend/database/create_database.sql
```

Depois altere o `.env` para:

```text
DATABASE_URL=mysql+pymysql://root:sua_senha@localhost:3306/evento_db
```

## Rotas da API

| Método | Rota | Descrição |
|---|---|---|
| GET | `/eventos` | Lista todos os eventos |
| GET | `/eventos/<id>` | Busca um evento pelo id |
| GET | `/eventos/por-tipo?tipo_evento=Casamento` | Busca eventos por tipo usando Repository |
| POST | `/eventos` | Cadastra um evento |
| PUT | `/eventos/<id>` | Atualiza um evento |
| DELETE | `/eventos/<id>` | Remove um evento |

## Caso de uso com Repository

Este projeto também possui um exemplo de consulta que não é CRUD básico:

```text
buscar_eventos_por_tipo
```

Fluxo do caso de uso:

```text
Controller -> Service -> Repository -> CALL sp_eventos_por_tipo -> MySQL
```

Rota:

```text
GET /evento/por-disciplina?tipo_evento=Casamento
```

No MySQL, a procedure está no arquivo:

```text
backend/database/create_database.sql
```

Para facilitar testes locais com SQLite, o Repository possui uma consulta equivalente usando SQLAlchemy.

## Exemplo de JSON para cadastrar

```json
{
  "nome_evento": "Chá do Bebe",
  "tipo_evento": "Chá de bebe",
  "data_evento": "01/01/2027",
  "endereco_evento": "Rua do Bebe 123",
  "orcamento_evento": "2"
}
```
