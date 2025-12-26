from pydantic import BaseModel, IPvAnyAddress
from app.modules.server_registry.domain.entity.server_status import ServerStatus

class RegisterServerLocationRequest(BaseModel):
    registrator_id: int
    name: str
    password: str
    ip_address: IPvAnyAddress
    port: int
    status: ServerStatus =  ServerStatus.INACTIVE