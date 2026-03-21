from pydantic import BaseModel
from app.modules.server_health_ckeck.domain.enum.health_check_status import HealthCheckStatus


class UpdateServerCheckRequest(BaseModel):
    name: str
    command: str
    threshold: int
    operator: str
    unit: str | None = None
    check_status: HealthCheckStatus
