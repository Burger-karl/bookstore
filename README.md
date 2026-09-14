# Bookstore API

FastAPI + SQLModel + PostgreSQL (Render) + Alembic.

## Features

- Author and Book CRUD
- Author -> Books foreign key relationship
- PostgreSQL
- Alembic migrations
- Session authentication for write endpoints
- Swagger UI at `/docs`
- Health endpoint
- No `create_all()`
- No Docker

## Setup

### 1. Create and activate virtual environment

Windows Git Bash:

```bash
python -m venv .venv
source .venv/Scripts/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure environment

Copy `.env.example` to `.env`:

```bash
cp .env.example .env
```

Put your Render PostgreSQL connection string in `DATABASE_URL`.

Use the SQLAlchemy/psycopg form:

```text
postgresql+psycopg://USERNAME:PASSWORD@HOST:5432/DATABASE_NAME
```

### 4. Generate the first migration

```bash
alembic revision --autogenerate -m "create users authors and books"
```

### 5. Apply migrations

```bash
alembic upgrade head
```

### 6. Run API

```bash
uvicorn app.main:app --reload
```

Open:

- http://127.0.0.1:8000/docs
- http://127.0.0.1:8000/health

## Swagger test order

1. POST `/auth/register`
2. POST `/auth/login`
3. POST `/authors/`
4. POST `/books/`
5. Test GET/PUT/DELETE endpoints.

Login creates the session cookie. Swagger requests in the same browser session can then access protected write endpoints.

## Render deployment

Set these environment variables in Render:

```text
DATABASE_URL=<your Render PostgreSQL URL>
SECRET_KEY=<strong random secret>
SESSION_COOKIE_NAME=bookstore_session
SESSION_EXPIRE_SECONDS=3600
APP_ENV=production
```

Build command:

```text
pip install -r requirements.txt
```

Start command:

```text
alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

This runs migrations automatically before starting the application.

## Important

Never use:

```python
SQLModel.metadata.create_all(engine)
```

Schema changes should be handled through Alembic.
