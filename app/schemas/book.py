# from decimal import Decimal
# from pydantic import BaseModel, ConfigDict, Field


# class BookCreate(BaseModel):
#     title: str = Field(min_length=1, max_length=255)
#     isbn: str = Field(min_length=10, max_length=20)
#     price: Decimal = Field(gt=0, decimal_places=2)
#     published_year: int | None = Field(default=None, ge=1000, le=2100)
#     description: str | None = Field(default=None, max_length=2000)
#     author_id: int


# class BookUpdate(BaseModel):
#     title: str | None = Field(default=None, min_length=1, max_length=255)
#     isbn: str | None = Field(default=None, min_length=10, max_length=20)
#     price: Decimal | None = Field(default=None, gt=0, decimal_places=2)
#     published_year: int | None = Field(default=None, ge=1000, le=2100)
#     description: str | None = Field(default=None, max_length=2000)
#     author_id: int | None = None


# class BookRead(BaseModel):
#     model_config = ConfigDict(from_attributes=True)
#     id: int
#     title: str
#     isbn: str
#     price: Decimal
#     published_year: int | None
#     description: str | None
#     author_id: int



from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class BookCreate(BaseModel):
    title: str
    isbn: str
    price: Decimal
    published_year: int | None = None
    description: str | None = None
    author_id: int


class BookUpdate(BaseModel):
    title: str | None = None
    isbn: str | None = None
    price: Decimal | None = None
    published_year: int | None = None
    description: str | None = None
    author_id: int | None = None


class BookRead(BaseModel):
    id: int
    title: str
    isbn: str
    price: Decimal
    published_year: int | None
    description: str | None
    author: str

    model_config = ConfigDict(from_attributes=True)