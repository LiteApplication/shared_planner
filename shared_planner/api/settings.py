import datetime

from typing import Annotated
from fastapi import APIRouter, Body, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import select

from shared_planner.api.auth import CurrentAdmin, CurrentUser, CurrentToken
from shared_planner.api.shops import ShopWithoutTimeRanges
from shared_planner.db.models import Reservation, Shop, User, Token, Setting
from shared_planner.db.session import SessionLock

router = APIRouter(prefix="/settings", tags=["settings"])


@router.patch("/{name}", dependencies=[Depends(CurrentAdmin)])
def patch(name: str, value: str = Body(...)) -> Setting:
    with SessionLock() as session:
        setting = session.get(Setting, name)
        if setting is None:
            raise HTTPException(404, "error.admin.setting_not_found")

        setting.value = value
        session.add(setting)
        session.commit()
        session.refresh(setting)
    return setting


@router.get("/{name}")
def get(name: str, user: User = Depends(CurrentUser)) -> Setting:
    with SessionLock() as session:
        setting = session.get(Setting, name)
        if setting is None:
            raise HTTPException(404, "error.admin.setting_not_found")

        if setting.private and not user.admin:
            raise HTTPException(403, "error.admin.required")

    return setting


@router.get("/", dependencies=[Depends(CurrentAdmin)])
def list_settings() -> list[Setting]:
    with SessionLock() as session:
        statement = select(Setting)
        settings = session.exec(statement).scalars().all()

    return settings
