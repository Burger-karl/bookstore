from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select
from sqlalchemy.orm import selectinload

from app.database.session import get_session
from app.dependencies.auth import get_current_user
from app.models.author import Author
from app.models.book import Book
from app.models.user import User
from app.schemas.book import BookCreate, BookRead, BookUpdate

router = APIRouter(prefix="/books", tags=["Books"])


@router.post("/", response_model=BookRead, status_code=201)
def create_book(
    book: BookCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    # Check that the author exists
    author = session.get(Author, book.author_id)

    if not author:
        raise HTTPException(
            status_code=404,
            detail="Author not found",
        )

    # Check whether the ISBN already exists
    existing_book = session.exec(
        select(Book).where(Book.isbn == book.isbn)
    ).first()

    if existing_book:
        raise HTTPException(
            status_code=409,
            detail="A book with this ISBN already exists.",
        )

    # Create the book
    new_book = Book(
        title=book.title,
        isbn=book.isbn,
        price=book.price,
        published_year=book.published_year,
        description=book.description,
        author_id=book.author_id,
    )

    session.add(new_book)
    session.commit()
    session.refresh(new_book)

    return BookRead(
        id=new_book.id,
        title=new_book.title,
        isbn=new_book.isbn,
        price=new_book.price,
        published_year=new_book.published_year,
        description=new_book.description,
        author=author.name,
    )

@router.get("/", response_model=list[BookRead])
def get_books(session: Session = Depends(get_session)):
    statement = select(Book).options(selectinload(Book.author))
    books = session.exec(statement).all()

    return [
        BookRead(
            id=book.id,
            title=book.title,
            isbn=book.isbn,
            price=book.price,
            published_year=book.published_year,
            description=book.description,
            author=book.author.name,
        )
        for book in books
    ]

@router.get("/{book_id}", response_model=BookRead)
def get_book(book_id: int, session: Session = Depends(get_session)):
    statement = (
        select(Book)
        .where(Book.id == book_id)
        .options(selectinload(Book.author))
    )

    book = session.exec(statement).first()

    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    return BookRead(
        id=book.id,
        title=book.title,
        isbn=book.isbn,
        price=book.price,
        published_year=book.published_year,
        description=book.description,
        author=book.author.name,
    )

@router.put("/{book_id}", response_model=BookRead)
def update_book(
    book_id: int,
    book_data: BookUpdate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    # Find the book
    book = session.get(Book, book_id)

    if not book:
        raise HTTPException(
            status_code=404,
            detail="Book not found",
        )

    # Check author if author_id is being changed
    if book_data.author_id is not None:
        author = session.get(Author, book_data.author_id)

        if not author:
            raise HTTPException(
                status_code=404,
                detail="Author not found",
            )
    else:
        author = session.get(Author, book.author_id)

    # Check ISBN only if a new ISBN was provided
    if book_data.isbn is not None:
        existing_book = session.exec(
            select(Book).where(
                Book.isbn == book_data.isbn,
                Book.id != book_id,
            )
        ).first()

        if existing_book:
            raise HTTPException(
                status_code=409,
                detail="A book with this ISBN already exists.",
            )

    # Update only the fields provided
    update_data = book_data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(book, field, value)

    session.add(book)
    session.commit()
    session.refresh(book)

    # Get the current author
    author = session.get(Author, book.author_id)

    return BookRead(
        id=book.id,
        title=book.title,
        isbn=book.isbn,
        price=book.price,
        published_year=book.published_year,
        description=book.description,
        author=author.name,
    )

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
