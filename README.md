![CI](https://github.com/norrakillen-hash/url-shortener/actions/workflows/ci.yml/badge.svg)

# URL Shortener API

Сервис для сокращения ссылок и сбора статистики переходов. Написан на FastAPI с использованием асинхронного PostgreSQL.

## Стек технологий
* Python 3.12
* FastAPI
* PostgreSQL + SQLAlchemy (asyncpg)
* Alembic (миграции)
* Docker + Docker Compose

## Как запустить (через Docker)
1. Клонируйте репозиторий.
2. Создайте файл `.env` в корне (скопируйте из `.env.example`).
3. Запустите контейнеры:
   ```bash
   docker compose up --build -d
