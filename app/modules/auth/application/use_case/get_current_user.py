# app/core/security.py
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.modules.auth.infrastructure.sql_repository.user_repo import SqlUserRepository
from app.core.db_session import get_session


security = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    session=Depends(get_session)
):
    token = credentials.credentials
  
    # 👇 DB lookup — fresh user every time
    user_repo = SqlUserRepository(session)
    user = await user_repo.get_user_by_token(token)

    if not user:
        raise HTTPException(status_code=401, detail="User not found or inactive")
    
    return user
