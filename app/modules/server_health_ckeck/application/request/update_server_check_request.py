from pydantic import BaseModel
from app.modules.server_health_ckeck.domain.enum.health_check_status import HealthCheckStatus


class UpdateServerCheckRequest(BaseModel):
    name: str | None = None
    command: str | None = None
    threshold: int | None = None
    operator: str | None = None
    unit: str | None = None
    check_status: HealthCheckStatus | None = None
