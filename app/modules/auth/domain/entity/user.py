import enum
from pydantic import BaseModel
from typing import Optional


class Roles(enum.Enum):
    SUPERADMIN = "superadmin"
    ADMIN = "admin"
    USER = "user"

class User(BaseModel):
    id: str
    first_name: str
    last_name: str
    user_name: str
    email: str
    hashed_password: str
    roles: list[Roles]  
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False