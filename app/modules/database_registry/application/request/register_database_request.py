from pydantic import BaseModel

class RegisterDatabaseRequest(BaseModel):
    server_id: int              
    name: str             
    type: str                 
    host: str        
    port: int
    database_name: str   
    sid: str | None = None     
    service_name: str | None = None 
    username: str
    password: str