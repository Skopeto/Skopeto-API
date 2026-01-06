from datetime import datetime
from enum import Enum
from pydantic import BaseModel

class NotificationChannel(str, Enum):
    EMAIL = "email"
    SLACK = "slack"
    SMS = "sms"

class NotificationSubscriber(BaseModel):
    user_id: int
    user_name: str
    delivery_address_email: str
    notification_channel: NotificationChannel
    slack_webhook_url: str | None = None
    subscribed_at: datetime
    is_active : bool = True
