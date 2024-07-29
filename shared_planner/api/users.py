from typing import Annotated

from fastapi import APIRouter, Body, Depends, HTTPException
from pydantic import BaseModel
from sqlmodel import select

from shared_planner.api.auth import CurrentAdmin, CurrentToken, CurrentUser, UserResult
from shared_planner.db.models import Token, User
from shared_planner.db.session import SessionLock

router = APIRouter(prefix="/users", tags=["users"])


class UserCreate(BaseModel):
    """Data model for user creation"""

    email: str
    full_name: str
    password: str
    admin: bool = False


@router.post("/create")
def create_user(
    user_data: UserCreate,
    admin: Annotated[User, Depends(CurrentAdmin)],
) -> UserResult:
    """Create a new user"""
    with SessionLock() as session:
        new_user = User(**user_data.model_dump())
        new_user.set_password(user_data.password)
        session.add(new_user)
        session.commit()
        session.refresh(new_user)
    return UserResult.from_user(new_user)


@router.get("/list", dependencies=[Depends(CurrentAdmin)])
def list_users() -> list[UserResult]:
    """List all users"""
    with SessionLock() as session:
        statement = select(User)
        users = session.exec(statement).all()
        users = [UserResult.from_user(user) for user in users]
    return users


@router.get("/get/{user_id}", dependencies=[Depends(CurrentAdmin)])
def get_user(
    user_id: int,
) -> UserResult:
    """Get a specific user"""
    with SessionLock() as session:
        statement = select(User).where(User.id == user_id)
        user = session.exec(statement).first()
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
    return UserResult.from_user(user)


@router.delete("/delete/{user_id}", dependencies=[Depends(CurrentAdmin)])
def delete_user(user_id: int) -> UserResult:
    """Delete a specific user"""
    with SessionLock() as session:
        statement = select(User).where(User.id == user_id)
        user = session.exec(statement).first()
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        session.delete(user)
        session.commit()
    return UserResult.from_user(user)


@router.put("/update/{user_id}", dependencies=[Depends(CurrentAdmin)])
def update_user(user_id: int, user_data: UserCreate) -> UserResult:
    """Update a specific user"""
    with SessionLock() as session:
        statement = select(User).where(User.id == user_id)
        user = session.exec(statement).first()
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        user.email = user_data.email
        user.full_name = user_data.full_name

        session.add(user)
        session.commit()
        session.refresh(user)
    return UserResult.from_user(user)


@router.put("/me")
def update_me(
    current_password: Annotated[str, Body()],
    user_data: UserCreate,
    token: Annotated[Token, Depends(CurrentToken)],
) -> UserResult:
    """Update the current user"""
    with SessionLock() as session:
        statement = select(User).where(User.id == token.user_id)
        user = session.exec(statement).first()
        if user is None:
            print(token)
            raise HTTPException(status_code=404, detail="User not found")

        # Check that the current password is correct
        if not user.check_password(current_password):
            raise HTTPException(status_code=401, detail="Invalid password")

        # Check that the email is the same
        if user.email != user_data.email:
            raise HTTPException(status_code=400, detail="Cannot change email")

        user.full_name = user_data.full_name
        user.set_password(user_data.password)
        session.add(user)
        session.commit()
        session.refresh(user)
    return UserResult.from_user(user)


@router.get("/me")
def read_users_me(user: Annotated[User, Depends(CurrentUser)]) -> UserResult:
    """Get current user's profile"""
    return UserResult.from_user(user)


@router.put("/set_admin/{user_id}", dependencies=[Depends(CurrentAdmin)])
def set_admin(
    user_id: int, admin: bool, current_user: User = Depends(CurrentUser)
) -> UserResult:
    """Set a user as admin"""
    with SessionLock() as session:
        statement = select(User).where(User.id == user_id)
        user = session.exec(statement).first()
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")

        if user.id == current_user.id:
            raise HTTPException(
                status_code=400, detail="Cannot change own admin status"
            )

        user.admin = admin
        session.add(user)
        session.commit()
        session.refresh(user)
    return UserResult.from_user(user)


@router.post("/toggle_admin", dependencies=[Depends(CurrentToken)])
def DEBUG_toggle_admin(token: Annotated[Token, Depends(CurrentToken)]) -> UserResult:
    """Toggle a user's admin status"""
    with SessionLock() as session:
        statement = select(User).where(User.id == token.user_id)
        user = session.exec(statement).first()
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        user.admin = not user.admin
        session.add(user)
        session.commit()
        session.refresh(user)
    return UserResult.from_user(user)
