from typing import Optional
from pydantic import BaseModel, IPvAnyAddress
from app.modules.server_registry.domain.entity.server_status import ServerStatus

class UpdateServerRequest(BaseModel):
    name: Optional[str] = None
    password: Optional[str] = None
    ip_address: Optional[str] = None
    port: Optional[int] = None
    status: Optional[str] = None