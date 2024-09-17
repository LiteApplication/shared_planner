import re
from typing import Annotated

from fastapi import APIRouter, Depends, Form, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from sqlmodel import select

from shared_planner.db.models import Notification, Token, User
from shared_planner.db.session import SessionLock

router = APIRouter(prefix="/auth", tags=["auth"])

_oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


class UserResult(BaseModel):
    """Data model for getting a user profile"""

    id: int
    email: str
    full_name: str
    admin: bool
    group: str = ""

    @classmethod
    def from_user(cls, user: User) -> "UserResult":
        return cls(
            email=user.email,
            full_name=user.full_name,
            admin=user.admin,
            id=user.id,
            group=user.group,
        )


def CurrentToken(access_token: Annotated[str, Depends(_oauth2_scheme)]) -> Token:
    """Get the current token from the access token"""
    with SessionLock() as session:
        statement = select(Token).where(Token.access_token == access_token)
        token = session.exec(statement).first()

        if token is None:
            raise HTTPException(status_code=401, detail="error.token.invalid")

        if token.is_expired():
            session.delete(token)
            raise HTTPException(status_code=401, detail="error.token.expired")
    return token


def CurrentUser(access_token: Annotated[Token, Depends(CurrentToken)]) -> User:
    """Get the current user from the access token"""
    with SessionLock() as session:
        statement = select(User).where(User.id == access_token.user_id)
        user = session.exec(statement).first()

        if user is None:
            raise HTTPException(status_code=404, detail="error.auth.user_not_found")
    return user


def CurrentAdmin(user: Annotated[User, Depends(CurrentUser)]) -> User:
    """Get the current user from the access token"""
    if not user.admin:
        raise HTTPException(status_code=403, detail="error.admin.required")
    return user


@router.get("/me")
def read_users_me(user: Annotated[User, Depends(CurrentUser)]) -> UserResult:
    """Get current user's profile"""
    return UserResult.from_user(user)


@router.post("/login")
def login(
    credentials: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    with SessionLock() as session:
        statement = select(User).where(User.email == credentials.username)
        user = session.exec(statement).first()

        if user is None:
            raise HTTPException(status_code=404, detail="error.auth.user_not_found")
        if not user.check_password(credentials.password):
            raise HTTPException(status_code=401, detail="error.auth.invalid_password")

        token = Token.create_token(user)
        session.add(Notification.create(user, "notification.login"))
        session.add(token)
        session.commit()
        session.refresh(token)
    return token


@router.post("/register")
def register(
    email: Annotated[str, Form()],
    full_name: Annotated[str, Form()],
    password: Annotated[str, Form()],
    group: str = Form(default=None),
) -> Token:
    with SessionLock() as session:
        statement = select(User).where(User.email == email)
        if session.exec(statement).first() is not None:
            raise HTTPException(status_code=409, detail="error.auth.email_exists")

        if len(password) < 6:
            raise HTTPException(status_code=400, detail="error.auth.password_too_short")

        if len(full_name) < 3:
            raise HTTPException(
                status_code=400, detail="error.auth.full_name_too_short"
            )

        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise HTTPException(status_code=400, detail="error.auth.email_invalid")

        new_user = User(full_name=full_name, email=email, group=group, admin=False)
        new_user.set_password(password)
        session.add(new_user)

        token = Token.create_token(new_user)
        session.add(token)

        session.commit()
        session.refresh(token)
    return token


@router.post("/logout")
def logout(token: Annotated[Token, Depends(CurrentToken)]) -> str:
    with SessionLock() as session:
        token = session.get(Token, token.id)
        session.delete(token)
        session.commit()

    return "Logged out"
