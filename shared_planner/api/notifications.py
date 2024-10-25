from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select


from shared_planner.api.auth import CurrentUser
from shared_planner.db.models import Notification, User
from shared_planner.db.session import SessionLock

router = APIRouter(prefix="/notifications", tags=["notifications"])


@router.get("/count")
def count_notifications(user: User = Depends(CurrentUser)) -> int:
    with SessionLock() as session:
        count = Notification.count_unread(user, session)

    return count


@router.get("/list")
def list_notifications(user: User = Depends(CurrentUser)) -> list[Notification]:
    with SessionLock() as session:
        user = session.get(User, user.id)
        if user is None:
            raise HTTPException(404, "error.auth.user_not_found")

        if not user.admin:
            notifications = user.notifications
        else:
            # A bit more expensive, but we need to get the admin notifications too
            notifications = Notification.list_notifications(user, session)
    return notifications


@router.get("/unread")
def list_unread(user: User = Depends(CurrentUser)) -> list[Notification]:
    with SessionLock() as session:
        notifications = Notification.find_unread(user, session)
    return notifications


@router.delete("/id/{notification_id}")
def delete_notification(notification_id: int, user: User = Depends(CurrentUser)):
    with SessionLock() as session:
        notification = session.get(Notification, notification_id)
        if notification is None:
            raise HTTPException(404, "error.notification.not_found")

        if notification.user_id != user.id and not user.admin:
            raise HTTPException(403, "error.notification.not_allowed")

        session.delete(notification)
        session.commit()
    return notification


@router.delete("/all")
def delete_all_notifications(user: User = Depends(CurrentUser)):
    with SessionLock() as session:
        notifications = session.exec(
            select(Notification).where(Notification.user_id == user.id)
        ).all()
        for notification in notifications:
            session.delete(notification)
        session.commit()
    return notifications


@router.patch("/id/{notification_id}/read")
def mark_read(notification_id: int, user: User = Depends(CurrentUser)):
    with SessionLock() as session:
        notification = session.get(Notification, notification_id)
        if notification is None:
            raise HTTPException(404, "error.notification.not_found")

        if notification.user_id != user.id and not user.admin:
            raise HTTPException(403, "error.notification.not_allowed")

        notification.mark_read()
        session.add(notification)
        session.commit()
        session.refresh(notification)
    return notification


@router.patch("/id/{notification_id}/unread")
def mark_unread(notification_id: int, user: User = Depends(CurrentUser)):
    with SessionLock() as session:
        notification = session.get(Notification, notification_id)
        if notification is None:
            raise HTTPException(404, "error.notification.not_found")

        if notification.user_id != user.id and not user.admin:
            raise HTTPException(403, "error.notification.not_allowed")

        notification.mark_unread()
        session.add(notification)
        session.commit()
        session.refresh(notification)
    return notification


@router.patch("/all/read")
def mark_all_read(user: User = Depends(CurrentUser)):
    with SessionLock() as session:
        notifications: list[Notification] = (
            session.exec(select(Notification).where(Notification.user_id == user.id))
            .scalars()
            .all()
        )
        for notification in notifications:
            notification.mark_read()
            session.add(notification)
        session.commit()
        for notification in notifications:
            session.refresh(notification)

    return notifications
