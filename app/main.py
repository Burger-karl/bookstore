from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy import text
from sqlmodel import Session
from starlette.middleware.sessions import SessionMiddleware

from app.core.config import settings
from app.database.session import engine
from app.routers.auth import router as auth_router
from app.routers.authors import router as authors_router
from app.routers.books import router as books_router


@asynccontextmanager
async def lifespan(_: FastAPI):
    yield


app = FastAPI(
    title="Bookstore API",
    description="Bookstore API built with FastAPI, SQLModel, PostgreSQL and Alembic.",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    SessionMiddleware,
    secret_key=settings.secret_key,
    session_cookie=settings.session_cookie_name,
    max_age=settings.session_expire_seconds,
    httponly=True,
    samesite="lax",
    https_only=settings.app_env == "production",
)

app.include_router(auth_router)
app.include_router(authors_router)
app.include_router(books_router)


@app.get("/", tags=["Health"])
def root():
    return {"message": "Bookstore API is running."}


@app.get("/health", tags=["Health"])
def health_check():
    try:
        with Session(engine) as session:
            session.exec(text("SELECT 1"))
        return {"status": "healthy", "database": "connected"}
    except Exception:
        return {"status": "unhealthy", "database": "unavailable"}
