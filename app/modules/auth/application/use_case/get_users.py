
from app.modules.auth.domain.entity.user import User
from app.modules.auth.domain.repository.user_repository import UserRepositoryInterface


async def get_users_use_case(user_repository: UserRepositoryInterface) -> list[User] | None:
    users = await user_repository.get_users()
    return users
 