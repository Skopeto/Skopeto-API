from app.core.Exception import ApplicationException
from app.modules.auth.domain.repository.user_repository import UserRepositoryInterface

async def username_exists(username: str, user_repository: UserRepositoryInterface, exclude_user_id: int | None = None) -> None:
    existing_username = await user_repository.get_by_username(username=username)
    if existing_username and (exclude_user_id is None or existing_username.id != exclude_user_id):
        raise ApplicationException("Username already exists")