from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select

from app.database.session import get_session
from app.dependencies.auth import get_current_user
from app.models.author import Author
from app.models.book import Book
from app.models.user import User
from app.schemas.book import BookCreate, BookRead, BookUpdate

router = APIRouter(prefix="/books", tags=["Books"])


@router.post("/", response_model=BookRead, status_code=status.HTTP_201_CREATED)
def create_book(
    data: BookCreate,
    session: Session = Depends(get_session),
    _: User = Depends(get_current_user),
):
    if not session.get(Author, data.author_id):
        raise HTTPException(status_code=404, detail="Author not found.")

    book = Book(**data.model_dump())
    session.add(book)

    try:
        session.commit()
        session.refresh(book)
    except IntegrityError:
        session.rollback()
        raise HTTPException(status_code=409, detail="A book with this ISBN already exists.")

    return book


@router.get("/", response_model=list[BookRead])
def get_books(session: Session = Depends(get_session)):
    return session.exec(select(Book)).all()


@router.get("/{book_id}", response_model=BookRead)
def get_book(book_id: int, session: Session = Depends(get_session)):
    book = session.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found.")
    return book


@router.put("/{book_id}", response_model=BookRead)
def update_book(
    book_id: int,
    data: BookUpdate,
    session: Session = Depends(get_session),
    _: User = Depends(get_current_user),
):
    book = session.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found.")

    update_data = data.model_dump(exclude_unset=True)

    if "author_id" in update_data and not session.get(Author, update_data["author_id"]):
        raise HTTPException(status_code=404, detail="Author not found.")

    for key, value in update_data.items():
        setattr(book, key, value)

    session.add(book)

    try:
        session.commit()
        session.refresh(book)
    except IntegrityError:
        session.rollback()
        raise HTTPException(status_code=409, detail="A book with this ISBN already exists.")

    return book


@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(
    book_id: int,
    session: Session = Depends(get_session),
    _: User = Depends(get_current_user),
):
    book = session.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found.")

    session.delete(book)
    session.commit()
