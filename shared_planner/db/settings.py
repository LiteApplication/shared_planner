from shared_planner.db.models import Setting
from shared_planner.db.session import SessionLock


# key: (value, private)
DEFAULTS = {
    "email_confirm_reservation": (
        True,
        False,
    ),  # Send a confirmation email after each reservation
    "email_notification_before": (
        24,
        False,
    ),  # Send a reminder for the upcoming reservation n hours before, -1 to disable
    "base_domain": ("http://localhost:5173", True),
}


def init_settings():
    with SessionLock() as session:
        settings = [
            Setting(key=k, value=str(v), private=p) for k, (v, p) in DEFAULTS.items()
        ]

        session.add_all(settings)
        session.commit()

    return
