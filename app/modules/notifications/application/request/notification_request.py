from datetime import datetime
from pydantic import BaseModel, EmailStr

class NotificationSubscriberRequest(BaseModel):
    user_id: int
    user_name: str
    delivery_address_email: EmailStr
    slack_webhook_url: str | None = None
    notification_channel: str
    subscribed_at: datetime
    