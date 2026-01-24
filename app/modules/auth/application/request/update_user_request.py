import enum
from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class Roles(enum.Enum):
    SUPERADMIN = "superadmin"
    ADMIN = "admin"
    USER = "user"

class UpdateUserRequest(BaseModel):
    user_name: Optional[str] = Field(None, min_length=3, max_length=50)
    first_name: Optional[str] = Field(None, min_length=1, max_length=50)
    last_name: Optional[str] = Field(None, min_length=1, max_length=50)
    email: Optional[EmailStr] = None                                                                                                                                          
    current_password: Optional[str] = Field(None, min_length=6)                                                                                                               
    new_password: Optional[str] = Field(None, min_length=6) 
    is_active: Optional[bool] = None
    roles: Optional[Roles] = None