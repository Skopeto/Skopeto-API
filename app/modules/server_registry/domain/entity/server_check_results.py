from pydantic import BaseModel
from datetime import datetime
from enum import Enum

class HealthStatus(str, Enum):
    HEALTHY = "healthy"
    UNHEALTHY = "unhealthy"
    OFFLINE = "offline"
    ERROR = "error"
    
class ServerCheckResults(BaseModel):
    id: int | None = None
    server_id: int
    status: HealthStatus
    check_name: str
    value: float
    unit: str | None = None
    uptime: float | None = None
    checked_at: datetime