# Bookstore API Architecture

```text
                    ┌─────────────────────┐
                    │     Swagger UI      │
                    │       /docs         │
                    └──────────┬──────────┘
                               │ HTTP
                               ▼
                    ┌─────────────────────┐
                    │      FastAPI        │
                    │      main.py        │
                    └──────────┬──────────┘
                               │
             ┌─────────────────┼─────────────────┐
             ▼                 ▼                 ▼
      ┌────────────┐    ┌────────────┐    ┌────────────┐
      │   Auth     │    │  Authors   │    │   Books    │
      │  Sessions  │    │    CRUD    │    │    CRUD    │
      └────────────┘    └──────┬─────┘    └──────┬─────┘
                               │                  │
                               └────────┬─────────┘
                                        ▼
                              ┌──────────────────┐
                              │     SQLModel     │
                              │ Models + Session │
                              └────────┬─────────┘
                                       │
                                       ▼
                              ┌──────────────────┐
                              │ PostgreSQL Render │
                              └──────────────────┘

                              ┌──────────────────┐
                              │     Alembic      │
                              │    Migrations    │
                              └────────┬─────────┘
                                       │
                                       ▼
                              Database Schema
```

## Data relationship

```text
Author (1)
   │
   │
   ├──────── Book
   ├──────── Book
   └──────── Book

books.author_id → authors.id
```
