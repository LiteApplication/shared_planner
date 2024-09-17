import datetime
import json
from typing import TYPE_CHECKING
from sqlmodel import Field, SQLModel, Relationship, func, not_, or_, select
import bcrypt

if TYPE_CHECKING:
    from shared_planner.db.session import SessionLock


class User(SQLModel, table=True):
    """Represents a user in the database"""

    id: int = Field(primary_key=True, default=None)  # ID of the user
    full_name: str  # Displayed name
    email: str = Field(index=True, unique=True)  # Email of the user
    hashed_password: bytes  # Password hashed
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
        self.hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt)

    def check_password(self, password: str) -> bool:
        return bcrypt.checkpw(password.encode("utf-8"), self.hashed_password)


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

    @staticmethod
    def create_token(user: User) -> "Token":
        return Token(
            user=user,
            access_token=bcrypt.gensalt().decode("utf-8"),
            expires_at=datetime.datetime.now() + datetime.timedelta(days=1),
        )


class Setting(SQLModel, table=True):
    """Represents the settings in the database"""

    key: str = Field(primary_key=True)
    value: str
    private: bool = True

    def toInt(self):
        return int(self.value)

    def toBool(self):
        return self.value == "True"


class Notification(SQLModel, table=True):
    """Represents a notification to a user in the database"""

    id: int = Field(primary_key=True, default=None)
    user_id: int | None = Field(foreign_key="user.id", nullable=True)
    user: User | None = Relationship(back_populates="notifications")
    message: str  # Holds the message description (notification.upcoming_reservation)
    date: datetime.datetime  # Date at which the notification was created
    data: str | None = None  # Holds the variable data for the message (JSON string)
    is_reminder: bool = False  # Will get deleted after the user has seen it
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
        user: User,
        message: str,
        data: dict | None = None,
        route: str | None = None,
        is_reminder: bool = False,
        mail: bool = False,
    ) -> "Notification":
        return Notification(
            user=user,
            message=message,
            data=json.dumps(data) if data else None,
            route=route,
            date=datetime.datetime.now(),
            mail=mail,
            is_reminder=is_reminder,
        )

    @staticmethod
    def find_unread(user: User, session: "SessionLock") -> list["Notification"]:
        return session.exec(
            select(Notification).where(
                not_(Notification.read),
                or_(Notification.user_id == user.id, Notification.user_id is None),
            )
        ).all()

    @staticmethod
    def find_unsent(session: "SessionLock"):
        return session.exec(
            select(Notification).where(
                Notification.mail,
                not_(Notification.mail_sent),
            )
        ).all()

    @staticmethod
    def count_unread(user: User, session: "SessionLock") -> int:
        if user.admin:
            return session.exec(
                select(func.count(Notification.id)).where(
                    not_(Notification.read),
                    or_(Notification.user_id == user.id, Notification.user_id is None),
                )
            ).first()

        else:
            return session.exec(
                select(func.count(Notification.id)).where(
                    Notification.user_id == user.id, not_(Notification.read)
                )
            ).first()
