import base64
import datetime
import hashlib
import json
from typing import TYPE_CHECKING
from fastapi.exceptions import HTTPException
from sqlmodel import (
    Field,
    SQLModel,
    Relationship,
    func,
    not_,
    or_,
    and_,
    select,
    true,
    false,
)
import bcrypt
import secrets


if TYPE_CHECKING:
    from shared_planner.db.session import SessionLock


class User(SQLModel, table=True):
    """Represents a user in the database"""

    id: int = Field(primary_key=True, default=None)  # ID of the user
    full_name: str  # Displayed name
    email: str = Field(index=True, unique=True)  # Email of the user
    hashed_password: bytes = b""  # Password hashed
    admin: bool = False  # Is the user an admin
    group: str  # Group of the user
    reservations: list["Reservation"] = Relationship(
        back_populates="user", cascade_delete=True
    )
    tokens: list["Token"] = Relationship(back_populates="user", cascade_delete=True)
    notifications: list["Notification"] = Relationship(
        back_populates="user", cascade_delete=True
    )

    def set_password(self, password: str):
        salt = bcrypt.gensalt()
        # Pre-hash to get around the 72 characters limit of bcrypt
        pre_hash = base64.b64encode(hashlib.sha256(password.encode("utf-8")).digest())
        self.hashed_password = bcrypt.hashpw(pre_hash, salt)

    def check_password(self, password: str) -> bool:
        if not self.hashed_password:
            return False  # Timing attacks are possible here but only to know if the user is initialized
        pre_hash = base64.b64encode(hashlib.sha256(password.encode("utf-8")).digest())
        return bcrypt.checkpw(pre_hash, self.hashed_password)

    @staticmethod
    def get_admins(session: "SessionLock") -> list["User"]:
        return session.exec(select(User).where(User.admin == True)).all()  # noqa: E712


class Shop(SQLModel, table=True):
    """Represents a shop in the database"""

    id: int = Field(primary_key=True, default=None)  # ID of the shop
    name: str  # Name of the shop (displayed)
    location: str  # Location of the shop (displayed)
    maps_link: str  # Google Maps link of the shop
    description: str  # Description of the shop (displayed)
    volunteers: int  # Number of volunteers max in the shop
    min_time: int  # Minimum time for a reservation (in minutes)
    max_time: int  # Maximum time for a reservation (in minutes)
    available_from: datetime.datetime  # Date from which the shop is available
    available_until: datetime.datetime  # Date until which the shop is available
    open_ranges: list["OpeningTime"] = Relationship(
        back_populates="shop", cascade_delete=True
    )
    reservations: list["Reservation"] = Relationship(
        back_populates="shop", cascade_delete=True
    )


class OpeningTime(SQLModel, table=True):
    """Represents the opening time range of a shop in the database"""

    id: int = Field(primary_key=True, default=None)
    shop_id: int = Field(foreign_key="shop.id")
    shop: Shop = Relationship(back_populates="open_ranges")
    day: int  # Day of the week (0 = Monday, 6 = Sunday)
    start_time: datetime.time
    end_time: datetime.time


class Reservation(SQLModel, table=True):
    """Represents a reservation in the database"""

    id: int = Field(primary_key=True, default=None)
    user_id: int = Field(foreign_key="user.id")
    user: User = Relationship(back_populates="reservations")
    shop_id: int = Field(foreign_key="shop.id")
    shop: Shop = Relationship(back_populates="reservations")
    start_time: datetime.datetime
    end_time: datetime.datetime
    validated: bool = False
    reminder_sent: bool = False

    @staticmethod
    def find_unsent_reminders(
        session: "SessionLock", hours_before: int
    ) -> list["Reservation"]:
        time_before = datetime.datetime.now() + datetime.timedelta(hours=hours_before)
        return session.exec(
            select(Reservation).where(
                not_(Reservation.reminder_sent),
                Reservation.start_time < time_before,
            )
        ).all()

    def ics_data(self, cancel: bool = False, update: bool = False) -> dict:
        from shared_planner.db.settings import get

        return {
            "event_name": "Réservation chez " + self.shop.name,
            "start_time": self.start_time.strftime("%Y-%m-%d %H:%M"),
            "duration_minutes": (self.end_time - self.start_time).total_seconds() // 60,
            "description": f"Réservation chez {self.shop.name}\nCliquer pour ouvrir dans Google Maps : {self.shop.maps_link}",
            "location": self.shop.maps_link,
            "organizer": get("mail_from").value,
            "id": self.id,
            "cancel": cancel,
            "update": update,
        }


class Token(SQLModel, table=True):
    """Represents a token in the database"""

    id: int = Field(primary_key=True, default=None)
    user_id: int = Field(foreign_key="user.id")
    user: User = Relationship(back_populates="tokens")
    access_token: str
    expires_at: datetime.datetime
    token_type: str = "bearer"

    def is_expired(self) -> bool:
        return self.expires_at < datetime.datetime.now()

    def renew(self):
        from shared_planner.db.settings import get  # circular import

        self.expires_at = datetime.datetime.now() + datetime.timedelta(
            hours=get("token_validity").asInt()
        )

    @staticmethod
    def create_token(user: User) -> "Token":
        from shared_planner.db.settings import get  # circular import

        return Token(
            user=user,
            access_token=secrets.token_urlsafe(32),
            expires_at=datetime.datetime.now()
            + datetime.timedelta(hours=get("token_validity").asInt()),
        )


class Setting(SQLModel, table=True):
    """Represents the settings in the database"""

    key: str = Field(primary_key=True)
    value: str
    private: bool = True

    def asInt(self):
        return int(self.value)

    def asBool(self):
        if self.value not in ("True", "False"):
            raise ValueError(f"Setting '{self.key}' is not a boolean ({self.value})")
        return self.value == "True"


class Notification(SQLModel, table=True):
    """Represents a notification to a user in the database"""

    id: int = Field(primary_key=True, default=None)
    user_id: int | None = Field(foreign_key="user.id", nullable=True)
    user: User | None = Relationship(back_populates="notifications")
    message: str  # Holds the message description (notification.upcoming_reservation)
    date: datetime.datetime  # Date at which the notification was created
    data: str | None = None  # Holds the variable data for the message (JSON string)
    is_reminder: bool = False  # Will get aggregated by the mailer daemon
    read: bool = False  # Has the user seen the notification
    route: str | None = None  # Route to send the user to when clicking on the action

    mail: bool = False  # Should the notification be sent by mail
    mail_sent: bool = False  # Has the mail been sent by the scheduler

    def mark_read(self):
        self.read = True
        return

    def mark_unread(self):
        self.read = False
        return

    @staticmethod
    def create(
        user: User | None,  # None means admins
        message: str,
        data: dict | None = None,
        route: str | None = None,
        is_reminder: bool = False,
        mail: bool = False,
    ) -> "Notification":
        return Notification(
            user=user,
            message=message,
            data=json.dumps(data) if data else "{}",
            route=route,
            date=datetime.datetime.now(),
            mail=mail,
            is_reminder=is_reminder,
        )

    @staticmethod
    def find_unread(user: User, session: "SessionLock") -> list["Notification"]:
        return session.exec(
            select(Notification).where(
                or_(
                    Notification.user_id == user.id,
                    and_(
                        Notification.user_id == None,  # noqa: E711
                        true() if user.admin else false(),
                    ),
                ),
                not_(Notification.read),
                Notification.date < datetime.datetime.now(),
            )
        ).all()

    @staticmethod
    def find_unsent(session: "SessionLock"):
        return session.exec(
            select(Notification).where(
                Notification.mail,
                not_(Notification.mail_sent),
                Notification.date < datetime.datetime.now(),
            )
        ).all()

    @staticmethod
    def count_unread(user: User, session: "SessionLock") -> int:
        return session.exec(
            select(func.count(Notification.id)).where(
                or_(
                    Notification.user_id == user.id,
                    and_(
                        Notification.user_id == None,  # noqa: E711
                        true() if user.admin else false(),
                    ),
                ),
                not_(Notification.read),
                Notification.date < datetime.datetime.now(),
            )
        ).first()

    @staticmethod
    def list_notifications(user: User, session: "SessionLock") -> list["Notification"]:
        return session.exec(
            select(Notification).where(
                or_(
                    Notification.user_id == user.id,
                    and_(
                        Notification.user_id == None,  # noqa: E711
                        true() if user.admin else false(),
                    ),
                ),
                Notification.date < datetime.datetime.now(),
            )
        ).all()


class PasswordReset(SQLModel, table=True):
    """Represents a password reset request in the database"""

    id: int = Field(primary_key=True, default=None)
    user_id: int = Field(foreign_key="user.id")
    user: User = Relationship()
    token: str
    expires_at: datetime.datetime
    used: bool = False
    sent: bool = False

    @staticmethod
    def create(user: User, session: "SessionLock") -> "PasswordReset":
        # Import here to avoid circular import
        from shared_planner.db.settings import get

        # Check if there is already a reset request
        # resets = session.exec(
        #    select(func.count(PasswordReset.id)).where(
        #        PasswordReset.user_id == user.id,
        #        not_(PasswordReset.used),
        #        PasswordReset.expires_at > datetime.datetime.now(),
        #    )
        # ).first()

        # if resets > 0:
        #    raise HTTPException(status_code=400, detail="error.reset_request_exists")

        # Create the reset request
        return PasswordReset(
            user=user,
            token=secrets.token_urlsafe(32),
            expires_at=datetime.datetime.now()
            + datetime.timedelta(hours=get("reset_token_validity").asInt()),
        )

    @staticmethod
    def check_token(token: str, session: "SessionLock") -> "PasswordReset":
        result = session.exec(
            select(PasswordReset).where(PasswordReset.token == token)
        ).first()
        if result is None:
            raise HTTPException(
                status_code=404, detail="error.auth.invalid_reset_token"
            )

        if result.expires_at < datetime.datetime.now():
            raise HTTPException(
                status_code=400, detail="error.auth.expired_reset_token"
            )

        if result.used:
            raise HTTPException(status_code=400, detail="error.auth.used_reset_token")
        return result

    @staticmethod
    def use_token(token: str, password: str, session: "SessionLock") -> None:
        # Get the reset request
        reset: PasswordReset = PasswordReset.check_token(token, session)
        # Mark the token as used
        reset.used = True
        # Set the new password
        reset.user.set_password(password)
        # Commit to the database now to avoid any problems
        session.commit()
