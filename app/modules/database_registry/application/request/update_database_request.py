from typing import Optional
from pydantic import BaseModel

class UpdateDatabaseRequest(BaseModel):
    server_id: Optional[int] = None   
    name: Optional[str] = None       
    db_type: Optional[str] = None             
    host: Optional[str] = None 
    port: Optional[int] = None
    database_name: Optional[str] = None
    service_name: Optional[str] = None 
    username: Optional[str] = None   
    password: Optional[str] = None