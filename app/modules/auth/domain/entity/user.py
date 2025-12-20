from pydantic import BaseModel
from typing import Optional

class User(BaseModel):
    id: str
    first_name: str
    last_name: str
    username: str
    email: str
    hashed_password: str
    user_type: str  
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False