# Currency Rates ETL API

Сервис для загрузки, хранения и выдачи курсов валют.

Проект собирает курсы валют из публичного API ЦБ РФ, сохраняет данные в PostgreSQL,
кеширует последние значения в Redis и отдает их через FastAPI. Запуск ETL-процесса
планируется через Apache Airflow.

## Стек

- Python
- FastAPI
- PostgreSQL
- SQLAlchemy
- Alembic
- Redis
- Apache Airflow
- Docker Compose
- Pytest
- Ruff

## Статус

Проект в разработке. Сейчас добавлен базовый каркас приложения и healthcheck.

## Локальный запуск API

```bash
uvicorn app.main:app --reload
```

Проверка:

```bash
curl http://127.0.0.1:8000/health
```
