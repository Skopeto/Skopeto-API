from pydantic import BaseModel
from typing import Optional
from app.modules.server_registry.domain.entity.server_status import ServerStatus

class Server(BaseModel):
    id: Optional[int] = None
    name: str
    ssh_password_encrypted: str 
    ip_address: str
    port: int
    status: Optional[ServerStatus]
