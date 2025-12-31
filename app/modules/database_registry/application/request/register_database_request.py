from typing import Optional
from pydantic import BaseModel

class RegisterDatabaseRequest(BaseModel):
    server_id: int              
    name: str             
    db_type: str                 
    host: str        
    port: int
    database_name: Optional[str]    
    service_name: Optional[str]   
    username: str
    password: str