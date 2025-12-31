from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class Database(BaseModel):
    id: int | None = None
    server_id: int              
    name: str
    db_type: str                   
    host: str        
    port: int
    database_name: Optional[str]
    service_name: Optional[str]
    username: str
    encrypted_password: str
    created_at: datetime