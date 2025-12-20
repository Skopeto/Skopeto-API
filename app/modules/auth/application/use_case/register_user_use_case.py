from app.modules.auth.application.request.register_user_request import RegisterUserRequest
from app.modules.auth.domain.entity.user import User
from app.modules.auth.domain.repository.user_repository import UserRepositoryInterface
from passlib.context import CryptContext

crypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return crypt_context.hash(password)

def user_exists(username: str, email: str, user_repository: UserRepositoryInterface) -> bool:
    existing_user = user_repository.get_by_username_or_email(username=username, email=email)
    if existing_user:
        raise Exception(f"User with username '{username}' or email '{email}' already exists.")
    return True

def register_user_use_case(request: RegisterUserRequest, user_repository: UserRepositoryInterface) -> User:
    user_exists(username=request.user_name, email=request.email, user_repository=user_repository)

    data = request.model_dump()
    data["password"] = hash_password(data["password"])
    data["user_type"] = data["user_type"].value

    return user_repository.persist(User(**data))