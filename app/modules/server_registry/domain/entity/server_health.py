from pydantic import BaseModel
from datetime import datetime
from enum import Enum

class HealthStatus(str, Enum):
    HEALTHY = "healthy"
    UNHEALTHY = "unhealthy"
    OFFLINE = "offline"
    
class ServerHealth(BaseModel):
    id: int | None = None
    server_id: int
    status: HealthStatus
    cpu_usage: float | None = None
    memory_usage: float | None = None
    disk_usage: float | None = None
    uptime: str | None = None
    checked_at: datetime