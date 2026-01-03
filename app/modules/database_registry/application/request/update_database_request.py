from typing import Optional
from pydantic import BaseModel

class UpdateDatabaseRequest(BaseModel):
    server_id: Optional[int]            
    name: Optional[str]               
    db_type: Optional[str]                 
    host: Optional[str]         
    port: Optional[int]
    database_name: Optional[str]    
    service_name: Optional[str]   
    username: Optional[str]   
    password: Optional[str]   