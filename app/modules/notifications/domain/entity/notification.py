from datetime import datetime
from pydantic import BaseModel

class Notification(BaseModel):
    id: int | None = None
    user_id: int
    title: str
    message: str
    created_at: datetime
    is_read: bool = False
    