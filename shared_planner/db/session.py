import datetime
import json
from sqlmodel import Session as _Session, SQLModel, create_engine
from sqlalchemy import Engine
from shared_planner.db.models import User, Shop, OpeningTime, Reservation, Token
from threading import Lock


class SessionLock:
    __instance = None

    engine: Engine
    db_mutex: Lock = Lock()

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super(SessionLock, cls).__new__(cls)
            cls.__instance.engine = create_engine("sqlite:///database.db")
        return cls.__instance

    def __enter__(self) -> _Session:
        self.db_mutex.acquire()
        return _Session(self.engine).__enter__()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.db_mutex.release()
        return _Session(self.engine).__exit__(exc_type, exc_val, exc_tb)

    def create_db_and_tables(self):
        SQLModel.metadata.create_all(self.engine)

    def load_dummies(self):
        SQLModel.metadata.drop_all(self.engine)
        SQLModel.metadata.create_all(self.engine)

        with open("dummy_data.json") as f:
            data = json.load(f)
        users = data["users"]
        for user in users:
            user["hashed_password"] = bytes(user["hashed_password"], "utf-8")
        shops = data["shops"]
        for shop in shops:
            shop["available_from"] = datetime.datetime.strptime(
                shop["available_from"], "%Y-%m-%d %H:%M:%S"
            )
            shop["available_until"] = datetime.datetime.strptime(
                shop["available_until"], "%Y-%m-%d %H:%M:%S"
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

        with self as session:
            print("Adding data")
            for user in users:
                session.add(User(**user))
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
