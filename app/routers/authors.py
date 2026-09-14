from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from app.database.session import get_session
from app.dependencies.auth import get_current_user
from app.models.author import Author
from app.models.user import User
from app.schemas.author import AuthorCreate, AuthorRead, AuthorUpdate

router = APIRouter(prefix="/authors", tags=["Authors"])


@router.post("/", response_model=AuthorRead, status_code=status.HTTP_201_CREATED)
def create_author(
    data: AuthorCreate,
    session: Session = Depends(get_session),
    _: User = Depends(get_current_user),
):
    author = Author(**data.model_dump())
    session.add(author)
    session.commit()
    session.refresh(author)
    return author


@router.get("/", response_model=list[AuthorRead])
def get_authors(session: Session = Depends(get_session)):
    return session.exec(select(Author)).all()


@router.get("/{author_id}", response_model=AuthorRead)
def get_author(author_id: int, session: Session = Depends(get_session)):
    author = session.get(Author, author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found.")
    return author


@router.put("/{author_id}", response_model=AuthorRead)
def update_author(
    author_id: int,
    data: AuthorUpdate,
    session: Session = Depends(get_session),
    _: User = Depends(get_current_user),
):
    author = session.get(Author, author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found.")

    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(author, key, value)

    session.add(author)
    session.commit()
    session.refresh(author)
    return author


@router.delete("/{author_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_author(
    author_id: int,
    session: Session = Depends(get_session),
    _: User = Depends(get_current_user),
):
    author = session.get(Author, author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found.")

    session.delete(author)
    session.commit()
