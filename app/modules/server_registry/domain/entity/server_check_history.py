from pydantic import BaseModel
from datetime import datetime
from app.modules.server_registry.domain.entity.server_check_results import HealthStatus


class ServerCheckHistory(BaseModel):
    id: int | None = None
    server_id: int
    status: HealthStatus
    check_name: str
    value: float
    unit: str | None = None
    uptime: float | None = None
    checked_at: datetime
