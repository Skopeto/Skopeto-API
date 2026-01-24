import logging
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from app.core.Exception import ApplicationException
from app.core.security import get_current_user, get_user_repository
from app.modules.auth.application.request.update_user_request import UpdateUserRequest
from app.modules.auth.application.use_case.get_user import get_user_use_case
from app.modules.auth.application.use_case.get_users import get_users_use_case
from app.modules.auth.application.use_case.update_user import update_user_use_case
from app.modules.auth.domain.entity.user import Roles
from app.modules.auth.domain.repository.user_repository import UserRepositoryInterface
from app.services.check_user_superadmin import check_if_user_superadmin

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/users", tags=["Users"])

class UserResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    user_name: str
    email: str
    roles: list[Roles]
    is_active: bool
    is_superuser: bool
    
    class Config:
        from_attributes = True
        
@router.get('')
async def get_users(
    current_user = Depends(get_current_user),
    user_repository: UserRepositoryInterface = Depends(get_user_repository)
) -> dict:
    users = await get_users_use_case(user_repository)
    if not users:
        raise ApplicationException("Users not found")
    
    user_responses = [UserResponse.model_validate(user) for user in users]
    return {"status": "success", "data": user_responses}

@router.get('/{user_id}')
async def get_user(
    user_id: int,
    current_user = Depends(get_current_user),
    user_repository: UserRepositoryInterface = Depends(get_user_repository)
):
    user = await get_user_use_case(user_id, user_repository)
    if not user:
        raise ApplicationException("Users not found")
    return {"status": "success", "data": user}

@router.patch("/{user_id}")
async def update_user(
    request: UpdateUserRequest,
    user_id: int,
    current_user=Depends(get_current_user),
    user_repository: UserRepositoryInterface = Depends(get_user_repository),
):
    user = await user_repository.get_user(user_id)
    if not user:
        raise ApplicationException("User not found")

    if current_user.id != user.id:
        await check_if_user_superadmin(current_user)

    if request.roles is not None:
        await check_if_user_superadmin(current_user)

    updated_user = await update_user_use_case(user_id, request, user_repository)

    return {"status": "success", "data": updated_user}


@router.patch('/manage/{user_id}')
async def manage_user(
    request: UpdateUserRequest,
    user_id: int,
    current_user = Depends(get_current_user),
    user_repository: UserRepositoryInterface = Depends(get_user_repository),
):
    await check_if_user_superadmin(current_user)

    user = await update_user_use_case(user_id, request, user_repository)
    if not user:
        raise ApplicationException("Users not found")
    return {"status": "success", "data": user}


