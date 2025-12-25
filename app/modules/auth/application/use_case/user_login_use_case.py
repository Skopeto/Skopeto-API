from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from app.core.Exception import ApplicationException, SecurityException
from app.modules.auth.application.request.login_request import LoginRequest
from app.modules.auth.application.service.create_access_token import create_access_token
from app.modules.auth.domain.entity.token import Token
from app.modules.auth.domain.repository.user_repository import UserRepositoryInterface
from datetime import datetime, timedelta, timezone

password_hasher = PasswordHasher()

def user_login_use_case(
    request: LoginRequest,
    user_repository: UserRepositoryInterface,
) -> dict:
    user = user_repository.get_by_username(request.username)
    
    if not user:
        raise SecurityException("Invalid username credentials")
    
    try:
        password_hasher.verify(user.hashed_password, request.password)
    except VerifyMismatchError:
        raise SecurityException("Invalid password credentials")
    
    access_token = create_access_token(user, expires_delta=timedelta(hours=24))
    
    if not access_token:
        raise ApplicationException('Access token not created')
    
    token = Token(
        access_token=access_token,
        token_type="bearer",
        expires_at=(datetime.now(timezone.utc) + timedelta(hours=24)).isoformat(),
        user_id=user.id
    )
    
    return token.model_dump()