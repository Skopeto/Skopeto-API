from pydantic import BaseModel
from typing import Optional

class Server(BaseModel):
    id: str
    name: str
    password: str 
    ip_address: str
    port: int
    status: Optional[str] = "offline"
