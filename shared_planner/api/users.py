from typing import Annotated

from fastapi import APIRouter, Body, Depends, HTTPException
from pydantic import BaseModel
from sqlmodel import select

from shared_planner.api.auth import CurrentAdmin, CurrentToken, CurrentUser, UserResult
from shared_planner.db.models import PasswordReset, Token, User
from shared_planner.db.session import SessionLock

router = APIRouter(prefix="/users", tags=["users"])


class UserCreate(BaseModel):
    """Data model for user creation"""

    email: str
    full_name: str
    password: str
    group: str
    admin: bool = False


@router.post("/create")
def create_user(
    user_data: UserCreate,
    admin: Annotated[User, Depends(CurrentAdmin)],
) -> UserResult:
    """Create a new user"""
    with SessionLock() as session:
        # Check if the user already exists
        statement = select(User).where(User.email == user_data.email)
        user = session.exec(statement).first()
        if user is not None:
            raise HTTPException(status_code=400, detail="error.user.already_exists")

        new_user = User(**user_data.model_dump())
        new_user.set_password(user_data.password)
        session.add(new_user)
        session.commit()
        session.refresh(new_user)
    return UserResult.from_user(new_user)


@router.post("/request_password_reset")
def reset_password(email: str) -> None:
    """Reset a user's password"""
    with SessionLock() as session:
        statement = select(User).where(User.email == email)
        user = session.exec(statement).first()
        if user is None:
            return  # Do not raise an error to prevent email enumeration
        # Create a new password reset request
        reset = PasswordReset.create(user, session)
        session.add(reset)
        session.commit()
    return


@router.post("/validate_token")
def validate_token(token: str) -> False:
    """Validate a password reset token"""
    with SessionLock() as session:
        result = PasswordReset.is_valid_token(token, session)
        if not result:
            raise HTTPException(status_code=400, detail="error.invalid_token")

    return True


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
            raise HTTPException(status_code=404, detail="error.user.not_found")
    return UserResult.from_user(user)


@router.delete("/delete/{user_id}", dependencies=[Depends(CurrentAdmin)])
def delete_user(user_id: int) -> UserResult:
    """Delete a specific user"""
    with SessionLock() as session:
        statement = select(User).where(User.id == user_id)
        user = session.exec(statement).first()
        if user is None:
            raise HTTPException(status_code=404, detail="error.user.not_found")
        session.delete(user)
        session.commit()
    return UserResult.from_user(user)


@router.put("/update")
def update_user(
    user_data: UserResult, exec_user: User = Depends(CurrentAdmin)
) -> UserResult:
    """Update a specific user"""
    with SessionLock() as session:
        statement = select(User).where(User.id == user_data.id)
        user = session.exec(statement).first()
        if user is None:
            raise HTTPException(status_code=404, detail="error.user.not_found")
        user.email = user_data.email
        user.full_name = user_data.full_name
        if user_data.id == exec_user.id:
            if user_data.admin != exec_user.admin:
                raise HTTPException(
                    status_code=400, detail="error.user.cant_set_self_admin"
                )
        user.admin = user_data.admin
        user.full_name = user_data.full_name
        user.email = user_data.email
        user.group = user_data.group

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
            raise HTTPException(status_code=404, detail="error.user.not_found")

        # Check that the current password is correct
        if not user.check_password(current_password):
            raise HTTPException(status_code=401, detail="error.auth.invalid_password")

        # Check that the email is the same
        if user.email != user_data.email:
            raise HTTPException(status_code=400, detail="error.user.email_not_same")

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


# TODO: REMOVE THIS
@router.post("/toggle_admin", dependencies=[Depends(CurrentToken)])
def DEBUG_toggle_admin(token: Annotated[Token, Depends(CurrentToken)]) -> UserResult:
    """Toggle a user's admin status"""
    with SessionLock() as session:
        statement = select(User).where(User.id == token.user_id)
        user = session.exec(statement).first()
        if user is None:
            raise HTTPException(status_code=404, detail="error.user.not_found")
        user.admin = not user.admin
        session.add(user)
        session.commit()
        session.refresh(user)
    return UserResult.from_user(user)
