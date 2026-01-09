from datetime import datetime
from enum import Enum
from pydantic import BaseModel, EmailStr

class NotificationChannel(str, Enum):
    EMAIL = "email"
    SLACK = "slack"
    SMS = "sms"

class NotificationSubscriber(BaseModel):
    id: int | None = None
    user_id: int
    user_name: str
    first_name: str | None = None
    last_name: str | None = None
    delivery_address_email: EmailStr | None = None
    notification_channel: NotificationChannel
    slack_webhook_url: str | None = None
    subscribed_at: datetime
    is_active : bool = True
