from pydantic import BaseModel
from app.modules.server_health_ckeck.domain.enum.health_check_status import HealthCheckStatus

class ServerCheck(BaseModel):
    health_check_id: int | None = None
    name : str
    command: str
    threshold: int
    operator: str
    check_status: HealthCheckStatus
