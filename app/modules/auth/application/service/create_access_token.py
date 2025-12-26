from datetime import datetime, timedelta, timezone
from jose import jwt
import os
from app.modules.auth.domain.entity.user import User

SECRET_KEY = os.getenv("JWT_SECRET_KEY", "dev-secret-key")
ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")

def create_access_token(user: User, expires_delta: timedelta) -> str:
    to_encode = {
        "user_id": user.id,
        "username": user.user_name
    }
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt