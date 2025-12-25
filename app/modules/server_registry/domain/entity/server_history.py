from pydantic import BaseModel
from datetime import datetime
from enum import Enum

class HealthStatushistory(str, Enum):
    HEALTHY = "healthy"
    UNHEALTHY = "unhealthy"
    OFFLINE = "offline"
    ERROR = "error"
    
class ServerHistory(BaseModel):
    id: int | None = None
    server_id: int
    status: HealthStatushistory
    cpu_usage: float | None = None
    memory_usage: float | None = None
    disk_usage: float | None = None
    uptime: str | None = None
    checked_at: datetime