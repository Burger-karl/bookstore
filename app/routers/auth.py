from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlmodel import Session, select

from app.core.security import hash_password, verify_password
from app.database.session import get_session
from app.models.user import User
from app.schemas.user import LoginRequest, UserCreate

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(data: UserCreate, session: Session = Depends(get_session)):
    if session.exec(select(User).where(User.username == data.username)).first():
        raise HTTPException(status_code=409, detail="Username already exists.")

    user = User(username=data.username, password_hash=hash_password(data.password))
    session.add(user)
    session.commit()
    session.refresh(user)

    return {"message": "User registered successfully.", "username": user.username}


@router.post("/login")
def login(
    data: LoginRequest,
    request: Request,
    session: Session = Depends(get_session),
):
    user = session.exec(select(User).where(User.username == data.username)).first()

    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password.",
        )

    request.session.clear()
    request.session["user_id"] = user.id
    return {"message": "Login successful.", "username": user.username}


@router.post("/logout")
def logout(request: Request):
    request.session.clear()
    return {"message": "Logout successful."}
