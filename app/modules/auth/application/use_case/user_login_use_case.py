from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from app.modules.auth.application.service.create_access_token import create_access_token
from app.modules.auth.domain.entity.token import Token
from app.modules.auth.domain.entity.user import User
from app.modules.auth.domain.repository.user_repository import UserRepositoryInterface
from datetime import datetime, timedelta

password_hasher = PasswordHasher()

def user_login_use_case(
    username: str, 
    password: str, 
    user_repository: UserRepositoryInterface,
) -> dict:
    user = user_repository.get_by_username(username)
    
    if not user:
        raise Exception("Invalid username")
    
    try:
        password_hasher.verify(user.hashed_password, password)
    except VerifyMismatchError:
        raise Exception("Invalid password")
    
    access_token = create_access_token(user, expires_delta=timedelta(hours=24))
    
    token = Token(
        access_token=access_token,
        token_type="bearer",
        expires_at=(datetime.now() + timedelta(hours=24)).isoformat(),
        user_id=user.id
    )
    
    return token.model_dump()