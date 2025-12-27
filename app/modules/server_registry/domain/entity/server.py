from pydantic import BaseModel, Field
from typing import Optional
from app.modules.server_registry.domain.entity.server_status import ServerStatus

class Server(BaseModel):
    id: Optional[int] = None
    user_name: str
    ssh_password_encrypted: str = Field(exclude=True)  # Exclude from JSON responses
    ip_address: str
    port: int
    status: Optional[ServerStatus]
