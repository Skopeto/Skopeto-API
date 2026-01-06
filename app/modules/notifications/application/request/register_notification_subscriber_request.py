from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr

class RegisterNotificationSubscriberRequest(BaseModel):
    user_id: int
    user_name: str
    delivery_address_email: Optional[EmailStr] = None
    slack_webhook_url: Optional[str] | None = None
    notification_channel: str
    subscribed_at: Optional[datetime] = None
