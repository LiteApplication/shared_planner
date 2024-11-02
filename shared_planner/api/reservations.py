import datetime

from typing import Annotated
from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from sqlmodel import select

from shared_planner.api.auth import CurrentAdmin, CurrentUser, CurrentToken
from shared_planner.api.shops import ShopWithoutTimeRanges
from shared_planner.db.models import Reservation, Shop, User, Token, Notification
from shared_planner.db.session import SessionLock
from shared_planner.db.settings import get
from shared_planner.week import monday_str

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
        cls, reservation: Reservation, user: User | None
    ) -> "ReservedTimeRange":
        if user is not None and reservation.user_id == user.id:
            status = -2
            title = "message.reservation.booked_by_you"
        elif user is None or user.admin:
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


class NewReservation(BaseModel):
    start_time: datetime.datetime
    duration_minutes: int
    user_id: int
    shop_id: int
    validated: bool = False


@router.get("/{shop_id}/{monday}/list")
def get_planning(
    shop_id: int, monday: str, user: Annotated[User, Depends(CurrentUser)]
) -> list[list[ReservedTimeRange]]:
    """Get the planning of a shop for a specific week

    A week is defined by the Monday of the week.
    The user is not allowed to see who booked a specific time range, but can see
    the number of available spaces. The user can see the time ranges they booked
    """
    with SessionLock() as session:
        shop = session.get(Shop, shop_id)
        if shop is None:
            raise HTTPException(status_code=404, detail="error.shop.not_found")

        # Ensure the day is a Monday
        week_start = datetime.datetime.strptime(monday, "%Y-%m-%d")

        if week_start.weekday() != 0:
            raise HTTPException(status_code=400, detail="error.reservation.not_monday")

        # load the time ranges of the shop
        used_ranges = shop.reservations

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

    if start_time < datetime.datetime.now() and not user.admin:
        raise HTTPException(status_code=400, detail="error.reservation.past_time")

    if start_time < shop.available_from and not user.admin:
        raise HTTPException(status_code=400, detail="error.reservation.before_open")

    if start_time > shop.available_until and not user.admin:
        raise HTTPException(status_code=400, detail="error.reservation.after_close")

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
        if not user.admin:
            raise HTTPException(
                status_code=400, detail="error.reservation.outside_open"
            )


@router.post("/{shop_id}/book")
def book_time_range(
    shop_id: int,
    start_time: datetime.datetime = Body(),
    duration_minutes: int = Body(),
    user: User = Depends(CurrentUser),
) -> ReservedTimeRange:
    """Book a time range in a shop"""
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

        session.add(
            Notification.create(
                user,
                "notification.reservation_created",
                {
                    "shop": shop.name,
                    "datetime-start_time": start_time.strftime("%Y-%m-%d %H:%M"),
                    "duration": duration.total_seconds() // 60,
                    "ics": new_reservation.ics_data(),
                },
                route=f"/shops/{shop.id}/{monday_str(start_time)}",
                is_reminder=False,
                # Do not send a mail if we are going to send a reminder anyway
                mail=get("email_reservation_created").asBool()
                and (
                    datetime.datetime.now()
                    < (
                        start_time
                        - datetime.timedelta(
                            hours=get("email_notification_before").asInt()
                        )
                    )
                ),
            )
        )

        if get("notif_admin_reservation_created").asBool() and (
            get("notify_for_admin_actions").asBool() or not user.admin
        ):
            session.add(
                Notification.create(
                    None,
                    "notification.admin.reservation_created",
                    {
                        "user": user.full_name,
                        "shop": shop.name,
                        "datetime-start_time": start_time.strftime("%Y-%m-%d %H:%M"),
                        "duration": duration_minutes,
                    },
                    route=f"/shops/{shop.id}/{monday_str(start_time)}",
                    is_reminder=True,
                    mail=get("email_admin_reservation_created").asBool(),
                )
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

        previous_start_time = reservation.start_time
        previous_duration = (
            reservation.end_time - reservation.start_time
        ).total_seconds() // 60

        if (
            start_time == reservation.start_time
            and duration_minutes == previous_duration
        ):
            # No change, no need to update
            return ReservedTimeRange.from_reservation(reservation, user)

        reservation.start_time = start_time
        reservation.end_time = start_time + datetime.timedelta(minutes=duration_minutes)
        session.add(reservation)
        session.commit()
        session.refresh(reservation)

        session.add(
            Notification.create(
                reservation.user,
                "notification.reservation_modified",
                {
                    "shop": reservation.shop.name,
                    "datetime-start_time": reservation.start_time.strftime(
                        "%Y-%m-%d %H:%M"
                    ),
                    "duration": duration_minutes,
                    "datetime-previous_start_time": previous_start_time.strftime(
                        "%Y-%m-%d %H:%M"
                    ),
                    "previous_duration": previous_duration,
                    "ics": reservation.ics_data(update=True),
                },
                route=f"/shops/{reservation.shop.id}/{monday_str(start_time)}",
                is_reminder=False,
                mail=get("email_reservation_modified").asBool(),
            )
        )

        if get("notif_admin_reservation_modified").asBool() and (
            get("notify_for_admin_actions").asBool() or not user.admin
        ):
            session.add(
                Notification.create(
                    None,
                    "notification.admin.reservation_modified",
                    {
                        "user": user.full_name,
                        "shop": reservation.shop.name,
                        "datetime-start_time": reservation.start_time.strftime(
                            "%Y-%m-%d %H:%M"
                        ),
                        "duration": duration_minutes,
                        "datetime-previous_start_time": previous_start_time.strftime(
                            "%Y-%m-%d %H:%M"
                        ),
                        "previous_duration": previous_duration,
                    },
                    route=f"/shops/{reservation.shop.id}/{monday_str(start_time)}",
                    is_reminder=False,
                    mail=get("email_admin_reservation_modified").asBool(),
                )
            )

        session.commit()
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

        session.add(
            Notification.create(
                reservation.user,
                "notification.reservation_cancelled",
                {
                    "shop": reservation.shop.name,
                    "datetime-start_time": reservation.start_time.strftime(
                        "%Y-%m-%d %H:%M"
                    ),
                    "duration": (
                        reservation.end_time - reservation.start_time
                    ).total_seconds()
                    // 60,
                    "ics": reservation.ics_data(cancel=True),
                },
                route=f"/shops/{reservation.shop.id}/{monday_str(reservation.start_time)}",
                is_reminder=False,
                mail=get("email_reservation_cancelled").asBool(),
            )
        )

        if get("notif_admin_reservation_cancelled").asBool() and (
            get("notify_for_admin_actions").asBool() or not user.admin
        ):
            session.add(
                Notification.create(
                    None,
                    "notification.admin.reservation_cancelled",
                    {
                        "user": user.full_name,
                        "shop": reservation.shop.name,
                        "datetime-start_time": reservation.start_time.strftime(
                            "%Y-%m-%d %H:%M"
                        ),
                        "duration": (
                            reservation.end_time - reservation.start_time
                        ).total_seconds()
                        // 60,
                    },
                    route=f"/shops/{reservation.shop.id}/{monday_str(reservation.start_time)}",
                    is_reminder=False,
                    mail=get("email_admin_reservation_cancelled").asBool(),
                )
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


@router.get("/list_self_future")
def get_user_future_reservations(
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
                for res in filter(
                    lambda res: res.end_time > datetime.datetime.now(),
                    user.reservations,
                )
            ],
            key=lambda res: res.start_time,
        )
    return reservations


@router.post("/search", dependencies=[Depends(CurrentAdmin)])
def search(
    shop_id: int | None = Body(None),
    user_id: int | None = Body(None),
    monday: str | None = Body(None),
) -> list[ReservedTimeRange]:
    """Search the database for reservations.

    If a search criteria is None, it is ignored.
    """
    with SessionLock() as session:
        query = select(Reservation)
        if shop_id is not None:
            query = query.where(Reservation.shop_id == shop_id)
        if user_id is not None:
            query = query.where(Reservation.user_id == user_id)
        if monday is not None:
            week_start = datetime.datetime.strptime(monday, "%Y-%m-%d")
            week_end = week_start + datetime.timedelta(days=7)
            query = query.where(
                Reservation.start_time >= week_start, Reservation.start_time < week_end
            )
        reservations = session.exec(query)

        result = [ReservedTimeRange.from_reservation(res, None) for res in reservations]

    return result


@router.put("/{reservation_id}/reassign", dependencies=[Depends(CurrentAdmin)])
def reassign_reservation(
    reservation_id: int,
    user_id: int = Body(...),
) -> ReservedTimeRange:
    """Reassign a reservation to a different user"""
    with SessionLock() as session:
        reservation = session.get(Reservation, reservation_id)
        if reservation is None:
            raise HTTPException(status_code=404, detail="error.reservation.not_found")
        user = session.get(User, user_id)
        if user is None:
            raise HTTPException(status_code=404, detail="error.user.not_found")
        reservation.user_id = user.id
        session.add(reservation)
        session.commit()
        session.refresh(reservation)

        session.add(
            Notification.create(
                user=reservation.user,
                message="notification.reservation_reassigned_old",
                data={
                    "shop": reservation.shop.name,
                    "datetime-start_time": reservation.start_time.strftime(
                        "%Y-%m-%d %H:%M"
                    ),
                    "duration": (
                        reservation.end_time - reservation.start_time
                    ).total_seconds()
                    // 60,
                    "ics": reservation.ics_data(cancel=True),
                },
                mail=True,
            )
        )
        session.add(
            Notification.create(
                user=user,
                message="notification.reservation_reassigned_new",
                data={
                    "shop": reservation.shop.name,
                    "datetime-start_time": reservation.start_time.strftime(
                        "%Y-%m-%d %H:%M"
                    ),
                    "duration": (
                        reservation.end_time - reservation.start_time
                    ).total_seconds()
                    // 60,
                    "ics": reservation.ics_data(),
                },
                route=f"/shops/{reservation.shop.id}/{monday_str(reservation.start_time)}",
                mail=True,
            )
        )
        session.commit()

        result = ReservedTimeRange.from_reservation(reservation, user)
    return result


@router.get("/all_data/{api_key}")
def get_all_data(api_key: str) -> str:
    """Get all the data from the database"""
    if get("api_key").value == "":
        raise HTTPException(status_code=403, detail="error.api_key_not_set")
    if api_key != get("api_key").value:
        raise HTTPException(status_code=403, detail="error.api_key_invalid")

    import csv
    from io import StringIO

    output = StringIO()

    with SessionLock() as session:
        # Dump all the reservations, the users and the shops associated, the duration of each reservation
        query = (
            select(Reservation)
            .order_by(Reservation.start_time)
            .order_by(Reservation.shop_id)
        )
        reservations = session.exec(query)
        writer = csv.DictWriter(
            output,
            fieldnames=[
                "shop_name",
                "user_name",
                "user_email",
                "user_group",
                "user_admin",
                "start_time",
                "duration",
            ],
        )
        writer.writeheader()
        for res in reservations:
            writer.writerow(
                {
                    "shop_name": res.shop.name,
                    "user_name": res.user.full_name,
                    "user_email": res.user.email,
                    "user_group": res.user.group,
                    "user_admin": res.user.admin,
                    "start_time": res.start_time,
                    "duration": (res.end_time - res.start_time).total_seconds()
                    / (60 * 60),  # in hours
                }
            )
    value = output.getvalue()
    output.close()
    response = StreamingResponse(content=iter([value]), media_type="text/csv")
    return response
