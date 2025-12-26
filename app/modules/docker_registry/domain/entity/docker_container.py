from pydantic import BaseModel, Field
from datetime import datetime
from app.modules.docker_registry.domain.entity.docker_status import ContainerStatus

class DockerContainer(BaseModel):
    id: int | None = None
    server_id: int
    container_id: str
    name: str
    image: str
    status: ContainerStatus
    ports: str
    exit_code: int | None = None
    state_changed_at: datetime | None = None
    is_healthy: bool | None = None
    last_seen_at: datetime | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None