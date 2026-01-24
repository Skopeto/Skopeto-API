from argon2 import PasswordHasher
from app.core.Exception import ApplicationException, SecurityException
from app.modules.auth.application.request.update_user_request import UpdateUserRequest
from app.modules.auth.domain.entity.user import User
from app.modules.auth.domain.repository.user_repository import UserRepositoryInterface
from argon2.exceptions import VerifyMismatchError

password_hasher = PasswordHasher()

async def update_user_use_case(user_id: int, request: UpdateUserRequest, user_repo: UserRepositoryInterface) -> User:
    existing_user = await user_repo.get_user(user_id)
    if not existing_user:
        raise ApplicationException("User not found")

    if request.user_name:
        other_user = await user_repo.get_by_username(request.user_name)
        if other_user and other_user.id != user_id:
            raise ApplicationException("Username already exists")

    if request.email:
        other_user = await user_repo.get_by_email(request.email)
        if other_user and other_user.id != user_id:
            raise ApplicationException("Email already exists")

    if request.current_password:
        try:
            password_hasher.verify(existing_user.hashed_password, request.current_password)
        except VerifyMismatchError:
            raise SecurityException("Current password is wrong")
    update_data = request.model_dump(exclude_unset=True)
    update_data.pop("current_password", None)

    if 'new_password' in update_data:
        update_data['hashed_password'] = password_hasher.hash(update_data.pop('new_password'))

    if "roles" in update_data and update_data["roles"] is not None:
        update_data["roles"] = update_data["roles"].value
    
    updated_user = existing_user.model_copy(update=update_data)
    
    return await user_repo.update_user(updated_user)