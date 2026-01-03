from typing import Optional
from pydantic import BaseModel

class UpdateServerRequest(BaseModel):
    name: Optional[str] = None
    password: Optional[str] = None
    ip_address: Optional[str] = None
    port: Optional[int] = None
    status: Optional[str] = None