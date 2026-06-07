from fastapi import APIRouter, Depends
from sqlalchemy import text

from database import engine
from auth_handler import verify_token

router = APIRouter()

# CREATE NOTIFICATION

@router.post("/")
def create_notification(
candidate_id: str,
message: str,
notification_type: str,
user=Depends(verify_token)):
    with engine.connect() as connection:
        connection.execute(
        text("""
            INSERT INTO notifications
            (
                candidate_id,
                message,
                notification_type,
                status
            )

            VALUES
            (
                :candidate_id,
                :message,
                :notification_type,
                'Unread'
            )
        """),
        {
            "candidate_id": candidate_id,
            "message": message,
            "notification_type": notification_type
        }
    )

    connection.commit()
    return {
    "message": "Notification Created"
}

# GET ALL NOTIFICATIONS

@router.get("/")
def get_notifications(
user=Depends(verify_token)):
    with engine.connect() as connection:
        result = connection.execute(
        text("""
            SELECT *
            FROM notifications
            ORDER BY created_at DESC
        """)
    )

    notifications = []

    for row in result:
        notifications.append(dict(row._mapping))

    return notifications


# GET NOTIFICATIONS OF CANDIDATE

@router.get("/{candidate_id}")
def get_candidate_notifications(
candidate_id: str,
user=Depends(verify_token)):
    with engine.connect() as connection:
        result = connection.execute(
        text("""
            SELECT *
            FROM notifications
            WHERE candidate_id = :candidate_id
            ORDER BY created_at DESC
        """),
        {
            "candidate_id": candidate_id
        }
    )

    notifications = []

    for row in result:
        notifications.append(dict(row._mapping))

    return notifications
