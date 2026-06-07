from pydantic import BaseModel


class Notification(BaseModel):

    candidate_id: str

    message: str

    notification_type: str

    status: str