from app.core.Exception import ApplicationException
from app.modules.auth.domain.entity.user import User
from app.modules.auth.domain.repository.user_repository import UserRepositoryInterface


async def get_user_use_case(user_id: int, user_repository: UserRepositoryInterface) -> User:
    user = await user_repository.get_user(user_id)
    if not user:
        raise ApplicationException(f"User {user_id} not found")
    return user  