from app.core.Exception import ApplicationException
from app.modules.auth.application.request.register_user_request import RegisterUserRequest
from app.modules.auth.domain.entity.user import Roles, User
from app.modules.auth.domain.repository.user_repository import UserRepositoryInterface
from argon2 import PasswordHasher

password_hasher = PasswordHasher()

def hash_password(password: str) -> str:
    truncated = password[:72]
    return password_hasher.hash(truncated)

async def user_exists(request: RegisterUserRequest, user_repository: UserRepositoryInterface) -> None:
    existing_user = await user_repository.get_by_username_or_email(
        username=request.user_name,
        email=request.email
    )
    
    if existing_user:
        raise ApplicationException(f"User with username '{request.user_name}' or email '{request.email}' already exists.")

async def register_user_use_case(request: RegisterUserRequest, user_repository: UserRepositoryInterface) -> User:
    await user_exists(request=request, user_repository=user_repository)
    
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