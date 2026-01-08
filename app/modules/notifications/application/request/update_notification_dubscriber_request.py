from typing import Optional
from pydantic import BaseModel, EmailStr

class UpdateNotificationSubscriberRequest(BaseModel):
    user_name: Optional[str] | None = None
    delivery_address_email: Optional[EmailStr] = None
    slack_webhook_url: Optional[str] | None = None
    notification_channel: Optional[str] | None = None
    is_active: Optional[bool] | None = None
