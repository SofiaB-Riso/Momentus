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

O **Momentus** é uma aplicação web desenvolvida com Laravel que permite cadastrar e gerenciar pequenos eventos.

O sistema foi criado com o objetivo de facilitar o planejamento de eventos, reunindo as principais informações em um único lugar.

---

# ✅ Funcionalidades Implementadas

- Cadastro de eventos
- Listagem de eventos
- Visualização dos detalhes de um evento
- Edição de eventos
- Exclusão de eventos

---

# 📦 Model Implementada

- Evento

---

# 🌐 Rotas CRUD

| Método | Rota | Função |
|---------|------|--------|
| GET | /eventos | Lista todos os eventos |
| GET | /eventos/create | Exibe o formulário de cadastro |
| POST | /eventos | Cadastra um novo evento |
| GET | /eventos/{evento} | Exibe um evento |
| GET | /eventos/{evento}/edit | Exibe o formulário de edição |
| PUT | /eventos/{evento} | Atualiza um evento |
| DELETE | /eventos/{evento} | Remove um evento |

---

# 🏗️ Arquitetura

O projeto foi desenvolvido utilizando o padrão **MVC (Model-View-Controller)** com Laravel.

Estrutura principal:

- Models
- Controllers
- Views (Blade)
- Rotas
- Migrations

---

# 🛠️ Tecnologias Utilizadas

## Back-end

- PHP
- Laravel

## Front-end

- HTML5
- CSS3
- JavaScript
- Blade

## Banco de Dados

- MySQL

---

# 📂 Estrutura do Projeto

```text
Momentus/
│
├── app/
│   ├── Http/
│   ├── Models/
│   └── ...
│
├── database/
│
├── public/
│
├── resources/
│   ├── views/
│   ├── css/
│   └── js/
│
├── routes/
│
└── README.md
```

---

# ▶️ Como Executar

## Pré-requisitos

- PHP 8 ou superior
- Composer
- MySQL

## Instalação

```bash
git clone <url-do-repositório>

cd Momentus

composer install

cp .env.example .env

php artisan key:generate

php artisan migrate

php artisan serve
```

A aplicação estará disponível em:

```
http://localhost:8000
```

---

# 🎯 Objetivo

Desenvolver uma aplicação capaz de facilitar o gerenciamento de pequenos eventos por meio das operações de cadastro, edição, visualização e exclusão de eventos.

---

# 📄 Licença

Projeto desenvolvido para fins acadêmicos.
