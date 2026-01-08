
from app.modules.auth.domain.entity.user import User
from app.modules.auth.domain.repository.user_repository import UserRepositoryInterface

async def get_user_use_case(user_id: int, user_repository: UserRepositoryInterface) -> User | None:
    return await user_repository.get_user(user_id)  