from shared_planner.db.models import Setting
from shared_planner.db.session import SessionLock


# key: (value, private?)
DEFAULTS = {
    "email_reservation_created": (
        True,
        False,
    ),  # Send a confirmation email after each reservation
    "email_reservation_modified": (
        True,
        False,
    ),  # Send an email when a reservation is modified
    "email_reservation_cancelled": (
        True,
        False,
    ),  # Send an email when a reservation is cancelled (to the user)
    "email_notification_before": (
        24,
        False,
    ),  # Send a reminder for the upcoming reservation n hours before, -1 to disable
    "base_domain": ("http://localhost:5173", True),  # Base domain for email links
    "notif_login": (False, True),  # Send notification when a user logs in
    "notif_reservation_created": (
        True,
        False,
    ),  # Send notification when a reservation is created
    "notif_admin_new_user_created": (
        False,
        True,
    ),  # Send notification to admin when a new user creates an account
    "email_admin_new_user_created": (
        False,
        True,
    ),  # Send email to admin when a new user creates an account
    "notif_new_user_created": (
        True,
        True,
    ),  # Send a welcome notification to the new users
    "notif_admin_reservation_created": (
        False,
        True,
    ),  # Send notification to admin when a reservation is created
    "notif_admin_reservation_modified": (
        True,
        True,
    ),  # Send notification to admin when a reservation is modified
    "notif_admin_reservation_cancelled": (
        True,
        True,
    ),  # Send notification to admin when a reservation is cancelled
    "email_admin_reservation_created": (
        False,
        True,
    ),  # Send email to admin when a reservation is created
    "email_admin_reservation_modified": (
        True,
        True,
    ),  # Send email to admin when a reservation is modified
    "email_admin_reservation_cancelled": (
        True,
        True,
    ),  # Send email to admin when a reservation is cancelled
    "email_daemon_delay": (1, True),  # Delay between email checks
    "reset_token_validity": (
        24,
        True,
    ),  # Time in hours for a password reset token to be valid
    "admin_mail": ("c.magaud@magev.fr", True),  # Email address for admin notifications
    "mail_from": ("OPC Notifications<opc@magev.fr>", True),  # Email sender
    "notify_for_admin_actions": (
        True,
        True,
    ),  # Should actions performed by admins be notified to other admins?
    "block_all_emails": (False, True),  # Block all emails
    "api_key": ("", True),  # API key to access the full data report
}


def init_settings():
    with SessionLock() as session:
        session.query(Setting).delete()
        settings = [
            Setting(key=k, value=str(v), private=p) for k, (v, p) in DEFAULTS.items()
        ]

        session.add_all(settings)
        session.commit()

    return


def get(name: str) -> Setting:
    with SessionLock() as session:
        setting = session.get(Setting, name)
        if setting is None:
            raise ValueError(f"Setting '{name}' not found")
    return setting
