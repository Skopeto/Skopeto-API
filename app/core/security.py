from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from app.modules.auth.domain.entity.user import User
from app.modules.auth.domain.repository.user_repository import UserRepositoryInterface
from app.modules.auth.infrastructure.sql_repository.user_repository import SqlUserRepository
from app.core.db_session import SessionDep
import os

SECRET_KEY = os.getenv("JWT_SECRET_KEY", "dev-secret-key")
ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")

security = HTTPBearer()

def get_user_repository(session: SessionDep) -> UserRepositoryInterface:
    return SqlUserRepository(session)

async def get_current_user(  # Make it async
    credentials: HTTPAuthorizationCredentials = Depends(security),
    user_repo: UserRepositoryInterface = Depends(get_user_repository)
) -> User:
    token = credentials.credentials
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")
        
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token")
            
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    user = await user_repo.get_user(user_id)  # Add await
    
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    
    return user