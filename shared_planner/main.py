from shared_planner.db.session import SessionLock, load_dummies
from shared_planner.db.models import Reservation, User, Shop
from shared_planner.db.settings import init_settings


import datetime


def main():
    load_dummies()

    with SessionLock() as session:
        shop_1 = session.get(Shop, 1)
        print(shop_1)

        user_3 = User(
            full_name="Alexis Rossfelder",
            email="123@liteapp.fr",
            hashed_password=b"password",
            admin=False,
            group="ADMIN",
        )
        user_3.set_password("secure_password")

        user_3.reservations.append(
            Reservation(
                shop=shop_1,
                start_time=datetime.datetime(2021, 1, 1, 12, 0),
                end_time=datetime.datetime(2021, 1, 1, 14, 0),
                status="accepted",
            )
        )
        session.add(user_3)
        session.commit()
        session.refresh(user_3)

        print("User 3 created")
        print("User:", user_3)
        print("Reservations:", user_3.reservations)
        print("First shop:", user_3.reservations[0].shop)
        print("Shoppenhower :", user_3.reservations[0].shop.open_ranges)

        init_settings()
