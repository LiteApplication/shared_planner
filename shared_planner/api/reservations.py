import datetime

from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlmodel import select

from shared_planner.api.auth import CurrentAdmin, CurrentToken, CurrentUser
from shared_planner.db.models import OpeningTime, Reservation, Shop, User
from shared_planner.db.session import SessionLock

router = APIRouter(prefix="/res", tags=["reservations"])


class ReservedTimeRange(BaseModel):
    """Data model for time range

    status :
    1 = someone booked
    2 = user booked

    if status <=0 then -status is the user id of the person who booked

    """

    id: int | None = None
    start_time: datetime.datetime
    duration: datetime.timedelta
    status: int
    validated: bool = False

    def from_reservation(reservation: Reservation, user: User) -> "ReservedTimeRange":
        if reservation.user_id == user.id:
            status = 2
        elif user.admin:
            status = -reservation.user_id
        else:
            status = 1

        return ReservedTimeRange(
            id=reservation.id,
            start_time=reservation.start_time,
            duration=reservation.end_time - reservation.start_time,
            status=status,
            validated=reservation.validated,
        )


@router.get("/list/{shop_id}/{year}/{week}")
def get_planning(
    shop_id: int, year: int, week: int, user: Annotated[User, Depends(CurrentUser)]
) -> list[list[ReservedTimeRange]]:
    """Get the planning of a shop for a specific week

    week is the number of the week in the year, starting on Monday
    The user is not allowed to see who booked a specific time range, but can see
    the number of available spaces. The user can see the time ranges they booked
    """
    with SessionLock() as session:
        shop = session.get(Shop, shop_id)
        if shop is None:
            raise HTTPException(status_code=404, detail="Shop not found")

        if week < 0 or week > 52:
            raise HTTPException(status_code=400, detail="Invalid week number")

        # load the time ranges of the shop
        used_ranges = shop.reservations
        week_start = datetime.datetime.strptime(f"{year}-W{week}-1", "%Y-W%W-%w")

        # Create a list of time ranges per day
        time_ranges = []
        for day in range(7):
            day_start = week_start + datetime.timedelta(days=day)
            day_end = day_start + datetime.timedelta(days=1)
            ranges = []
            for time_range in used_ranges:
                if time_range.start_time < day_start or time_range.end_time >= day_end:
                    continue
                ranges.append(ReservedTimeRange.from_reservation(time_range, user))
            time_ranges.append(ranges)

        return time_ranges


@router.post("/book/{shop_id}/{year}/{week}")
def book_time_range(
    shop_id: int,
    start_time: datetime.datetime,
    duration: datetime.timedelta,
    user: Annotated[User, Depends(CurrentUser)],
) -> ReservedTimeRange:
    """Book a time range in a shop for a specific week

    week is the number of the week in the year, starting on Monday
    """
    with SessionLock() as session:
        shop = session.get(Shop, shop_id)
        if shop is None:
            raise HTTPException(status_code=404, detail="Shop not found")

        # Check that the number of overlapping reservations is less than shop.volunteers
        overlap_check = []
        for reservation in shop.reservations:
            if (
                start_time <= reservation.start_time < start_time + duration
                or start_time < reservation.end_time <= start_time + duration
            ):
                overlap_check.append((1, reservation.start_time))
                overlap_check.append((-1, reservation.end_time))

        overlap_check.sort(key=lambda x: x[1])
        overlap_count = 0
        for change, _ in overlap_check:
            overlap_count += change
            if overlap_count > shop.volunteers:
                raise HTTPException(
                    status_code=400, detail="Too many overlapping reservations"
                )

        new_reservation = Reservation(
            user_id=user.id,
            shop=shop,
            start_time=start_time,
            end_time=start_time + duration,
        )
        session.add(new_reservation)
        session.commit()
        session.refresh(new_reservation)

    return ReservedTimeRange.from_reservation(new_reservation, user)


@router.delete("/cancel/{reservation_id}")
def cancel_reservation(
    reservation_id: int, user: Annotated[User, Depends(CurrentUser)]
) -> None:
    """Cancel a reservation"""
    with SessionLock() as session:
        reservation = session.get(Reservation, reservation_id)
        if reservation is None:
            raise HTTPException(status_code=404, detail="Reservation not found")
        if reservation.user_id != user.id or not user.admin:
            raise HTTPException(
                status_code=403, detail="Not allowed to cancel this reservation"
            )
        if reservation.validated:
            raise HTTPException(
                status_code=400, detail="Cannot cancel a validated reservation"
            )
        session.delete(reservation)
        session.commit()
    return None


@router.put("/validate/{reservation_id}", dependencies=[Depends(CurrentAdmin)])
def validate_reservation(reservation_id: int) -> ReservedTimeRange:
    """Validate a reservation"""
    with SessionLock() as session:
        reservation = session.get(Reservation, reservation_id)
        if reservation is None:
            raise HTTPException(status_code=404, detail="Reservation not found")
        reservation.validated = True
        session.add(reservation)
        session.commit()
        session.refresh(reservation)
    return ReservedTimeRange(
        id=reservation.id,
        start_time=reservation.start_time,
        duration=reservation.end_time - reservation.start_time,
        status=1,
    )


@router.get("/list/user/{user_id}", dependencies=[Depends(CurrentAdmin)])
def get_reservations(user_id: int) -> list[ReservedTimeRange]:
    """Get the reservations of a user"""
    with SessionLock() as session:
        user = session.get(User, user_id)
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        reservations = user.reservations
        return [
            ReservedTimeRange(
                id=reservation.id,
                start_time=reservation.start_time,
                duration=reservation.end_time - reservation.start_time,
                status=1 if reservation.validated else 2,
            )
            for reservation in reservations
        ]


@router.get("/list", dependencies=[Depends(CurrentUser)])
def get_user_reservations(
    user: Annotated[User, Depends(CurrentUser)],
) -> list[ReservedTimeRange]:
    """Get the reservations of the current user"""
    reservations = user.reservations
    return [
        ReservedTimeRange.from_reservation(reservation, user)
        for reservation in reservations
    ]
