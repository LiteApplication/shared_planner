import datetime

from typing import Annotated
from fastapi import APIRouter, Body, Depends, HTTPException
from pydantic import BaseModel

from shared_planner.api.auth import CurrentAdmin, CurrentUser, CurrentToken
from shared_planner.api.shops import ShopWithoutTimeRanges
from shared_planner.db.models import Reservation, Shop, User, Token
from shared_planner.db.session import SessionLock

router = APIRouter(prefix="/res", tags=["reservations"])


class ReservedTimeRange(BaseModel):
    """Data model for time range

    status :
    -1 = someone booked
    -2 = user booked

    if status => 0 then status is the user id of the person who booked.


    """

    id: int | None = None
    start_time: datetime.datetime
    duration_minutes: int
    status: int
    validated: bool = False
    title: str = ""
    shop: Shop | None = None

    @classmethod
    def from_reservation(
        cls, reservation: Reservation, user: User
    ) -> "ReservedTimeRange":
        if reservation.user_id == user.id:
            status = -2
            title = "message.reservation.booked_by_you"
        elif user.admin:
            status = reservation.user_id
            title = f"{reservation.user.full_name} ({reservation.user.group})"
        else:
            status = -1
            title = "message.reservation.booked"

        return cls(
            id=reservation.id,
            start_time=reservation.start_time,
            duration_minutes=(
                reservation.end_time - reservation.start_time
            ).total_seconds()
            // 60,
            status=status,
            validated=reservation.validated,
            title=title,
            shop=ShopWithoutTimeRanges.from_shop(reservation.shop),
        )


@router.get("/{shop_id}/{year}/{week}/list")
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
            raise HTTPException(status_code=404, detail="error.shop.not_found")

        if week < 0 or week > 52:
            raise HTTPException(status_code=400, detail="error.shop.invalid_week")

        # load the time ranges of the shop
        used_ranges = shop.reservations

        week_start = datetime.datetime.strptime(f"{year}-W{week}-1", "%Y-W%W-%w")

        # Create a list of time ranges per day
        time_ranges: list[ReservedTimeRange] = []
        for day in range(7):
            day_start = week_start + datetime.timedelta(days=day)
            day_end = day_start + datetime.timedelta(days=1)
            ranges = []
            for time_range in used_ranges:
                if time_range.start_time < day_start or time_range.end_time >= day_end:
                    continue
                ranges.append(ReservedTimeRange.from_reservation(time_range, user))
            time_ranges.append(ranges)
        session.close()

    return time_ranges


def check_overlap(
    shop: Shop,
    start_time: datetime.datetime,
    duration: datetime.timedelta,
    user: User,
    exclude_res_id: int = None,
):
    """Check if a reservation overlaps with too much existing reservations or with a specific user.

    Returns True if the reservation is valid, False otherwise."""
    overlap_check = []
    end_time = start_time + duration
    for reservation in shop.reservations:
        if (
            start_time <= reservation.start_time < end_time
            or start_time < reservation.end_time <= end_time
        ) and reservation.id != exclude_res_id:
            overlap_check.append((1, reservation.start_time))
            overlap_check.append((-1, reservation.end_time))
            if reservation.user_id == user.id:
                return False

    overlap_check.sort(key=lambda x: x[1])
    overlap_count = 0
    for change, _ in overlap_check:
        overlap_count += change
        if overlap_count > shop.volunteers:
            return False
    return True


def check_reservation(
    shop: Shop,
    start_time: datetime.datetime,
    duration_minutes: int,
    user: User,
    exclude_res_id: int = None,
) -> None:
    """Check if a reservation is valid

    Returns True if the reservation is valid, False otherwise."""
    duration = datetime.timedelta(minutes=duration_minutes)
    if not (
        check_overlap(shop, start_time, duration, user, exclude_res_id=exclude_res_id)
        or user.admin
    ):
        raise HTTPException(status_code=400, detail="error.reservation.overlap")

    if duration_minutes < shop.min_time and not (user.admin and duration_minutes > 0):
        raise HTTPException(status_code=400, detail="error.reservation.too_short")

    if duration_minutes > shop.max_time and not user.admin:
        raise HTTPException(status_code=400, detail="error.reservation.too_long")

    # Get the day of the week
    day = start_time.weekday()

    # Check that the reservation fits inside a single open time range
    for open_time in shop.open_ranges:
        if (open_time.day != day) or (open_time.start_time > open_time.end_time):
            continue
        if (
            open_time.start_time <= start_time.time()
            and (start_time + duration).time() <= open_time.end_time
        ):
            break
    else:
        raise HTTPException(status_code=400, detail="error.reservation.outside_open")


@router.post("/{shop_id}/book")
def book_time_range(
    shop_id: int,
    start_time: datetime.datetime = Body(),
    duration_minutes: int = Body(),
    user: User = Depends(CurrentUser),
) -> ReservedTimeRange:
    """Book a time range in a shop for a specific week

    week is the number of the week in the year, starting on Monday
    """
    with SessionLock() as session:
        shop = session.get(Shop, shop_id)
        if shop is None:
            raise HTTPException(status_code=404, detail="error.shop.not_found")

        check_reservation(shop, start_time, duration_minutes, user)

        duration = datetime.timedelta(minutes=duration_minutes)

        new_reservation = Reservation(
            user_id=user.id,
            shop=shop,
            start_time=start_time,
            end_time=start_time + duration,
        )
        session.add(new_reservation)
        session.commit()
        session.refresh(new_reservation)

        result = ReservedTimeRange.from_reservation(new_reservation, user)
    return result


@router.put("/{reservation_id}/update")
def update_reservation(
    reservation_id: int,
    start_time: datetime.datetime = Body(),
    duration_minutes: int = Body(),
    user: User = Depends(CurrentUser),
) -> ReservedTimeRange:
    """Update a reservation"""
    with SessionLock() as session:
        reservation = session.get(Reservation, reservation_id)
        if reservation is None:
            raise HTTPException(status_code=404, detail="error.reservation.not_found")
        if reservation.user_id != user.id and not user.admin:
            raise HTTPException(status_code=403, detail="error.reservation.cant_update")
        if reservation.validated and not user.admin:
            raise HTTPException(
                status_code=400, detail="error.reservation.cant_update_validated"
            )

        start_time = start_time.replace(second=0, microsecond=0)

        check_reservation(
            reservation.shop,
            start_time,
            duration_minutes,
            user,
            exclude_res_id=reservation.id,
        )

        reservation.start_time = start_time
        reservation.end_time = start_time + datetime.timedelta(minutes=duration_minutes)
        session.add(reservation)
        session.commit()
        session.refresh(reservation)
        result = ReservedTimeRange.from_reservation(reservation, user)
    return result


@router.delete("/{reservation_id}/cancel")
def cancel_reservation(
    reservation_id: int, user: Annotated[User, Depends(CurrentUser)]
) -> None:
    """Cancel a reservation"""
    with SessionLock() as session:
        reservation = session.get(Reservation, reservation_id)
        if reservation is None:
            raise HTTPException(status_code=404, detail="error.reservation.not_found")
        if reservation.user_id != user.id and not user.admin:
            raise HTTPException(status_code=403, detail="error.reservation.cant_cancel")
        if reservation.validated and not user.admin:
            raise HTTPException(
                status_code=400, detail="error.reservation.cant_cancel_validated"
            )
        session.delete(reservation)
        session.commit()
    return None


@router.put("/{reservation_id}/validate", dependencies=[Depends(CurrentAdmin)])
def validate_reservation(reservation_id: int) -> ReservedTimeRange:
    """Validate a reservation"""
    with SessionLock() as session:
        reservation = session.get(Reservation, reservation_id)
        if reservation is None:
            raise HTTPException(status_code=404, detail="error.reservation.not_found")
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


@router.get("/{user_id}/list_user", dependencies=[Depends(CurrentAdmin)])
def get_reservations(user_id: int) -> list[ReservedTimeRange]:
    """Get the reservations of a user"""
    with SessionLock() as session:
        user = session.get(User, user_id)
        if user is None:
            raise HTTPException(status_code=404, detail="error.user.not_found")
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


@router.get("/list_self")
def get_user_reservations(
    token: Annotated[Token, Depends(CurrentToken)],
) -> list[ReservedTimeRange]:
    """Get the reservations of the current user"""
    with SessionLock() as session:
        user = session.get(User, token.user_id)
        if user is None:
            raise HTTPException(status_code=404, detail="error.user.not_found")
        reservations = sorted(
            [
                ReservedTimeRange.from_reservation(res, user)
                for res in user.reservations
            ],
            key=lambda res: res.start_time,
        )
    return reservations
