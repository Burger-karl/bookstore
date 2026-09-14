from typing import TYPE_CHECKING
from decimal import Decimal
from sqlmodel import Field, Relationship, SQLModel
from sqlalchemy import Numeric

if TYPE_CHECKING:
    from app.models.author import Author


class Book(SQLModel, table=True):
    __tablename__ = "books"

    id: int | None = Field(default=None, primary_key=True)
    title: str = Field(index=True, min_length=1, max_length=255)
    isbn: str = Field(unique=True, index=True, max_length=20)
    price: Decimal = Field(sa_type=Numeric(12, 2), gt=0)
    published_year: int | None = Field(default=None, ge=1000, le=2100)
    description: str | None = Field(default=None, max_length=2000)

    author_id: int = Field(
        foreign_key="authors.id",
        index=True,
        ondelete="CASCADE",
    )
    author: "Author" = Relationship(back_populates="books")
