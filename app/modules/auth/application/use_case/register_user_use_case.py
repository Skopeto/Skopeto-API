from app.core.Exception import ApplicationException
from app.modules.auth.application.request.register_user_request import RegisterUserRequest
from app.modules.auth.application.service.check_user_email import email_exists
from app.modules.auth.application.service.check_user_username import username_exists
from app.modules.auth.domain.entity.user import Roles, User
from app.modules.auth.domain.repository.user_repository import UserRepositoryInterface
from argon2 import PasswordHasher

password_hasher = PasswordHasher()

def hash_password(password: str) -> str:
    truncated = password[:72]
    return password_hasher.hash(truncated)


async def register_user_use_case(request: RegisterUserRequest, user_repository: UserRepositoryInterface) -> User:
    await username_exists(username=request.user_name, user_repository=user_repository)
    await email_exists(email=request.email, user_repository=user_repository)

    user = User(
        id=0,
        user_name=request.user_name,               
        first_name=request.first_name,
        last_name=request.last_name,
        email=request.email,
        hashed_password=hash_password(request.password), 
        roles=[Roles(request.user_type.value)]      
    )
    
    persisted_user = await user_repository.persist_user(user)
    
    if not persisted_user:
        raise ApplicationException('Failed to persist user')
    
    return persisted_user