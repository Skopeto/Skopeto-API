from app.core.Exception import ApplicationException
from app.modules.auth.domain.repository.user_repository import UserRepositoryInterface

async def email_exists(email: str, user_repository: UserRepositoryInterface, exclude_user_id: int | None = None) -> None:
    existing_email = await user_repository.get_by_email(email=email)
    if existing_email and (exclude_user_id is None or existing_email.id != exclude_user_id):
        raise ApplicationException("Email already exists")