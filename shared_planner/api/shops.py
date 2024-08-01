import datetime

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlmodel import select

from shared_planner.api.auth import CurrentAdmin, CurrentToken
from shared_planner.db.models import OpeningTime, Shop
from shared_planner.db.session import SessionLock

router = APIRouter(prefix="/shops", tags=["shops"])
timerange_router = APIRouter(prefix="/timeranges", tags=["timeranges"])


class ShopWithoutTimeRanges(BaseModel):
    """Data model for shop without time ranges."""

    id: int | None = None
    name: str
    description: str
    location: str
    latitude: float
    longitude: float
    volunteers: int
    available_from: datetime.datetime
    available_until: datetime.datetime


class ShopWithTimeRanges(ShopWithoutTimeRanges):
    """Data model for shop with time ranges."""

    open_ranges: list["TimeRange"]


class TimeRange(BaseModel):
    """Data model for time range"""

    id: int | None = None
    day: int
    start_time: datetime.time
    end_time: datetime.time


@router.get("/get/{shop_id}", dependencies=[Depends(CurrentToken)])
def get_shop(shop_id: int) -> ShopWithTimeRanges:
    """Get a specific shop"""
    with SessionLock() as session:
        shop = session.get(Shop, shop_id)
        if shop is None:
            raise HTTPException(status_code=404, detail="error.shop.not_found")

        result = ShopWithTimeRanges(
            open_ranges=[],
            **shop.model_dump(
                include=[
                    "id",
                    "name",
                    "description",
                    "location",
                    "latitude",
                    "longitude",
                    "volunteers",
                    "available_from",
                    "available_until",
                ]
            ),
        )

        for time_range in shop.open_ranges:
            result.open_ranges.append(
                TimeRange(
                    **time_range.model_dump(
                        include=[
                            "id",
                            "day",
                            "start_time",
                            "end_time",
                        ]
                    )
                )
            )

    return result


@router.get("/list", dependencies=[Depends(CurrentToken)])
def list_shops() -> list[ShopWithoutTimeRanges]:
    """List all shops"""
    with SessionLock() as session:
        statement = select(Shop)
        shops = session.exec(statement).all()
    return shops


@router.post("/create", dependencies=[Depends(CurrentAdmin)])
def create_shop(shop_data: ShopWithoutTimeRanges) -> Shop:
    """Create a new shop"""
    with SessionLock() as session:
        new_shop = Shop(**shop_data.model_dump())
        session.add(new_shop)
        session.commit()
        session.refresh(new_shop)
    return new_shop


@router.delete("/delete/{shop_id}", dependencies=[Depends(CurrentAdmin)])
def delete_shop(shop_id: int) -> None:
    """Delete a specific shop"""
    with SessionLock() as session:
        shop = session.get(Shop, shop_id)
        if shop is None:
            raise HTTPException(status_code=404, detail="error.shop.not_found")
        session.delete(shop)
        session.commit()
    return None


@router.put("/update/{shop_id}", dependencies=[Depends(CurrentAdmin)])
def update_shop(shop_id: int, shop_data: ShopWithoutTimeRanges) -> Shop:
    """Update a specific shop"""
    with SessionLock() as session:
        shop = session.get(Shop, shop_id)
        if shop is None:
            raise HTTPException(status_code=404, detail="error.shop.not_found")
        if shop_data.id is not None:
            if shop_data.id != shop.id:
                raise HTTPException(status_code=400, detail="error.shop.id_mismatch")
        else:
            shop_data.id = shop_id
        session.add(shop_data)
        session.commit()
        session.refresh(shop)
    return shop


@timerange_router.post("/create/{shop_id}", dependencies=[Depends(CurrentAdmin)])
def create_time_range(shop_id: int, time_range: TimeRange) -> OpeningTime:
    """Create a new time range for a shop"""
    with SessionLock() as session:
        shop = session.get(Shop, shop_id)
        if shop is None:
            raise HTTPException(status_code=404, detail="error.shop.not_found")

        # Check for overlapping time ranges
        for existing_time_range in shop.open_ranges:
            if existing_time_range.day == time_range.day:
                if (
                    existing_time_range.start_time <= time_range.start_time
                    and existing_time_range.end_time > time_range.start_time
                ) or (
                    existing_time_range.start_time < time_range.end_time
                    and existing_time_range.end_time >= time_range.end_time
                ):
                    raise HTTPException(
                        status_code=400,
                        detail="error.shop.time_range_overlap",
                    )
        # Check that the time range is longer than 0
        if time_range.start_time >= time_range.end_time:
            raise HTTPException(
                status_code=400, detail="error.shop.negative_time_range"
            )

        new_time_range = OpeningTime(shop=shop, **time_range.model_dump())
        session.add(new_time_range)
        session.commit()
        session.refresh(new_time_range)
    return new_time_range


@timerange_router.delete(
    "/delete/{time_range_id}", dependencies=[Depends(CurrentAdmin)]
)
def delete_time_range(time_range_id: int) -> None:
    """Delete a specific time range"""
    with SessionLock() as session:
        time_range = session.get(OpeningTime, time_range_id)
        if time_range is None:
            raise HTTPException(
                status_code=404, detail="error.shop.time_range_not_found"
            )
        session.delete(time_range)
        session.commit()
    return None


@timerange_router.put("/update/{time_range_id}", dependencies=[Depends(CurrentAdmin)])
def update_time_range(time_range_id: int, new_tr: TimeRange) -> OpeningTime:
    """Update a specific time range"""
    with SessionLock() as session:
        time_range = session.get(OpeningTime, time_range_id)
        if time_range is None:
            raise HTTPException(
                status_code=404, detail="error.shop.time_range_not_found"
            )

        time_range.day = new_tr.day
        time_range.start_time = new_tr.start_time
        time_range.end_time = new_tr.end_time

        session.add(time_range)
        session.commit()
        session.refresh(time_range)
    return time_range
