import datetime
from sqlmodel import Field, SQLModel, Relationship
import bcrypt


class User(SQLModel, table=True):
    """Represents a user in the database"""

    id: int = Field(primary_key=True, default=None)  # ID of the user
    full_name: str  # Displayed name
    email: str = Field(index=True, unique=True)  # Email of the user
    hashed_password: bytes  # Password hashed
    admin: bool = False  # Is the user an admin
    group: str  # Group of the user
    reservations: list["Reservation"] = Relationship(back_populates="user")
    tokens: list["Token"] = Relationship(back_populates="user")

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
    open_ranges: list["OpeningTime"] = Relationship(back_populates="shop")
    reservations: list["Reservation"] = Relationship(back_populates="shop")


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
