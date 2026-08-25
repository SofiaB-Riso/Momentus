# Backend Momentus

API Flask/SQLAlchemy do Momentus. Por padrão usa SQLite (`momentus.db`); para MySQL configure `DATABASE_URL` e execute `database/create_database.sql`.

## Instalação

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

A aplicação inteira fica disponível em `http://127.0.0.1:5000`.

## Segurança e persistência

- autenticação por cookie de sessão HttpOnly;
- senhas com hash do Werkzeug;
- dados de negócio no banco de dados;
- `localStorage` é usado apenas pelo frontend para preferências de interface.
