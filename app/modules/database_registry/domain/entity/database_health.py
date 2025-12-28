from enum import Enum
from datetime import datetime
from pydantic import BaseModel

class DatabaseHealthStatus(str, Enum):
    HEALTHY = "healthy"
    SLOW = "slow"           
    WARNING = "warning"     
    ERROR = "error"        
    OFFLINE = "offline"     

class DatabaseHealth(BaseModel):
    id: int | None = None
    database_id: int
    status: DatabaseHealthStatus
    connection_time_ms: float | None
    is_connected: bool
    query_time_ms: float | None           
    error_message: str | None              
    checked_at: datetime