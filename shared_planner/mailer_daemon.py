import os
import time
import threading
from queue import Queue
from dotenv import load_dotenv
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from shared_planner.db.models import Setting, Reservation, Notification
from shared_planner.db.settings import get
from shared_planner.db.session import SessionLock

# Load environment variables from .env file
load_dotenv()

SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), "..", "templates")

mail_queue = Queue()


def send_mail(name, email, template, data):
    with open(os.path.join(TEMPLATE_DIR, template) + ".html", "r") as file:
        template_content = file.read()

    for key, value in data.items():
        template_content = template_content.replace(f"{{{key}}}", str(value))

    msg = MIMEMultipart()
    msg["From"] = SMTP_USER
    msg["To"] = f"{name} <{email}>"
    msg["Subject"] = f"Reminder for {name}"

    msg.attach(MIMEText(template_content, "html"))

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.sendmail(SMTP_USER, email, msg.as_string())
            print(f"Email sent to {email}")
    except Exception as e:
        print(f"Failed to send email to {email}: {e}")


def queue_mail(name, email, template, data):
    mail_queue.put((name, email, template, data))


def queue_reminders():
    email_notification_before = get("email_notification_before").asInt()
    if email_notification_before == -1:
        return
    with SessionLock() as session:
        to_send = Reservation.find_unsent_reminders(session, email_notification_before)
        for reservation in to_send:
            Notification.create(
                user=reservation.user,
                message="reminder",
                data={
                    "base_domain": get("base_domain").value,
                    "date": reservation.date,
                    "duration": reservation.end_time - reservation.start_time,
                    "year": reservation.date.year,
                    "week": reservation.date.isocalendar()[1],
                },
                route=f"/shops/{reservation.shop_id}/{reservation.date.year}/{reservation.date.isocalendar()[1]}",
                is_reminder=True,
                mail=True,
            )


def queue_notifications():
    pass


def mailer_daemon():
    while True:
        if not mail_queue.empty():
            name, email, template, data = mail_queue.get()
            send_mail(name, email, template, data)
        time.sleep(get("email_daemon_delay").asInt())
        queue_reminders()
        queue_notifications()


def start_mailer_daemon():
    daemon_thread = threading.Thread(target=mailer_daemon, daemon=True)
    daemon_thread.start()


def main():
    start_mailer_daemon()
    queue_mail(
        "John Doe",
        "john.doe@liteapp.fr",
        "welcome",
        {"name": "John Doe", "date": "2023-10-01"},
    )
    # Keep the main thread alive
    while True:
        time.sleep(1)


# Example usage
if __name__ == "__main__":
    main()
