from pydantic import BaseModel, Field
from datetime import datetime

class SchedulerTimer(BaseModel):
    id: int | None = None
    interval_minutes: int = Field(default=5, ge=1, le=1440)
    created_at: datetime | None = None