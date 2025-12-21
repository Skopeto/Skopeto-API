import token
from app.modules.auth.application.request.register_user_request import RegisterUserRequest
from app.modules.auth.domain.entity.user import Roles, User
from app.modules.auth.domain.repository.user_repository import UserRepositoryInterface
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

password_hasher = PasswordHasher()

def hash_password(password: str) -> str:
    truncated = password[:72]
    return password_hasher.hash(truncated)

def verify_password(hashed_password: str, plain_password: str) -> bool:
    try:
        password_hasher.verify(hashed_password, plain_password)
        return True
    except VerifyMismatchError:
        return False

def user_exists(request: RegisterUserRequest, user_repository: UserRepositoryInterface) -> bool:
    existing_user = user_repository.get_by_username_or_email(
        username=request.user_name,
        email=request.email
    )
    if existing_user:
        raise Exception(f"User with username '{request.user_name}' or email '{request.email}' already exists.")
    return False

def register_user_use_case(request: RegisterUserRequest, user_repository: UserRepositoryInterface) -> User:
    user_exists(request=request, user_repository=user_repository)
    user = User(
        id=0,
        user_name=request.user_name,               
        first_name=request.first_name,
        last_name=request.last_name,
        email=request.email,
        hashed_password=hash_password(request.password), 
        roles=[Roles(request.user_type.value)]      
    )

    return user_repository.persist_user(user)