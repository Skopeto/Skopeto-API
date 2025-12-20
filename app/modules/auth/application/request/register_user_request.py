from pydantic import BaseModel, EmailStr, Field
from enum import Enum

class UserType(str, Enum):
    ADMIN = "admin"
    SUPERADMIN = "superadmin"
    REGULAR = "regular"

class RegisterUserRequest(BaseModel):
   user_name: str = Field(..., min_length=3, max_length=50)
   first_name: str = Field(..., min_length=1, max_length=50)
   last_name: str = Field(..., min_length=1, max_length=50)
   email: EmailStr
   password: str = Field(..., min_length=6)
   user_type: UserType 