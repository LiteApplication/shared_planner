import datetime
import json
from sqlmodel import SQLModel, create_engine, Session as _Session
from sqlalchemy import Engine
from shared_planner.db.models import (
    User,
    Shop,
    OpeningTime,
    Reservation,
    Token,
    Notification,
)


from contextlib import contextmanager


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super(Singleton, cls).__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class EngineContainer(metaclass=Singleton):
    engine: Engine

    def __init__(self):
        self.engine = create_engine(
            "sqlite:///database.db", pool_timeout=10, max_overflow=50, pool_size=5
        )
        SQLModel.metadata.create_all(self.engine)


@contextmanager
def SessionLock():
    session = _Session(EngineContainer().engine)
    try:
        yield session
    finally:
        session.close()


def load_dummies():
    engine = EngineContainer().engine

    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)

    with open("dummy_data.json") as f:
        data = json.load(f)
    users = data["users"]
    for user in users:
        user["hashed_password"] = bytes(user["hashed_password"], "utf-8")
    shops = data["shops"]
    for shop in shops:
        shop["available_from"] = datetime.datetime.strptime(
            shop["available_from"], "%Y-%m-%d"
        )
        shop["available_until"] = datetime.datetime.strptime(
            shop["available_until"], "%Y-%m-%d"
        )
    opening_times = data["opening_times"]
    for opening_time in opening_times:
        opening_time["start_time"] = datetime.datetime.strptime(
            opening_time["start_time"], "%H:%M"
        ).time()

        opening_time["end_time"] = datetime.datetime.strptime(
            opening_time["end_time"], "%H:%M"
        ).time()
    reservations = data["reservations"]
    for reservation in reservations:
        reservation["start_time"] = datetime.datetime.strptime(
            reservation["start_time"], "%Y-%m-%d %H:%M:%S"
        )
        reservation["end_time"] = datetime.datetime.strptime(
            reservation["end_time"], "%Y-%m-%d %H:%M:%S"
        )

    tokens = data["tokens"]
    for token in tokens:
        token["expires_at"] = datetime.datetime.strptime(
            token["expires_at"], "%Y-%m-%d %H:%M:%S"
        )

    with SessionLock() as session:
        print("Adding data")
        for user in users:
            u = User(**user)
            session.add(u)
            session.add(
                Notification.create(u, "notification.test", {"test": "test value"})
            )
            session.add(
                Notification.create(
                    u, "notification.test", {"test": "test reminder"}, is_reminder=True
                )
            )
        for shop in shops:
            session.add(Shop(**shop))
        for opening_time in opening_times:
            session.add(OpeningTime(**opening_time))
        for reservation in reservations:
            session.add(Reservation(**reservation))
        for token in tokens:
            session.add(Token(**token))

        print("Committing")

        session.commit()
