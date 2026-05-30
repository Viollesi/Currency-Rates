# Currency Rates ETL API

Проект для загрузки и выдачи курсов валют.

Сервис получает курсы из XML API ЦБ РФ
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

## Архитектура

```text
ЦБ РФ XML API
    |
    v
Airflow DAG -> ETL pipeline
    |
    +--> PostgreSQL: сырые XML-данные
    +--> PostgreSQL: нормализованные курсы
    +--> Redis: последние курсы
    |
    v
FastAPI -> /rates, /rates/{code}
```

Основные файлы:

- `app/main.py` — FastAPI endpoints.
- `app/cbr_client.py` — загрузка и парсинг XML от ЦБ РФ.
- `app/etl.py` — ETL pipeline.
- `app/repositories.py` — простой repository layer.
- `dags/currency_rates_dag.py` — Airflow DAG.

## Валюты

В первой версии загружаются:

```text
USD, EUR, CNY, GBP, JPY
```

## Запуск Через Docker Compose

Создайте `.env` на основе примера:

```bash
cp .env.example .env
```

Запустите инфраструктуру:

```bash
docker compose up --build
```

Сервисы:

- FastAPI: `http://localhost:8000`
- Swagger: `http://localhost:8000/docs`
- Airflow: `http://localhost:8080`
- PostgreSQL: `localhost:5432`
- Redis: `localhost:6379`

Логин в Airflow:

```text
admin / admin
```

## Миграции

После запуска контейнеров примените миграции:

```bash
docker compose exec api alembic upgrade head
```

## Запуск ETL

Откройте Airflow:

```text
http://localhost:8080
```

Запустите DAG:

```text
currency_rates_etl
```

После успешного запуска данные появятся в PostgreSQL и Redis.

## API

Проверка сервиса:

```bash
curl http://localhost:8000/health
```

Список последних курсов:

```bash
curl http://localhost:8000/rates
```

Курс конкретной валюты:

```bash
curl http://localhost:8000/rates/USD
```

Пример ответа:

```json
{
  "code": "USD",
  "name": "Доллар США",
  "nominal": 1,
  "value": 90.12,
  "rate_date": "2026-05-30"
}
```

## Локальный Запуск Без Docker

Установите зависимости:

```bash
pip install -r requirements.txt
```

Запустите API:

```bash
uvicorn app.main:app --reload
```

## Проверки

Тесты:

```bash
pytest
```

Ruff:

```bash
ruff check .
```

Проверка Docker Compose:

```bash
docker compose config
```

