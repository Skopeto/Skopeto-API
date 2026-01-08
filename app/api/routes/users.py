import logging
from fastapi import APIRouter, Depends
from app.core.Exception import ApplicationException
from app.core.security import get_user_repository
from app.modules.auth.application.use_case.get_user import get_user_use_case
from app.modules.auth.application.use_case.get_users import get_users_use_case
from app.modules.auth.domain.repository.user_repository import UserRepositoryInterface

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/users", tags=["Users"])

@router.get('')
async def get_users(
    user_repository: UserRepositoryInterface = Depends(get_user_repository)
):
    users = await get_users_use_case(user_repository)
    if not users:
        raise ApplicationException("Users not found")
    return {"status": "success", "data": users}

@router.get('/{user_id}')
async def get_user(
    user_id: int,
    user_repository: UserRepositoryInterface = Depends(get_user_repository)
):
    user = await get_user_use_case(user_id, user_repository)
    if not user:
        raise ApplicationException("Users not found")
    return {"status": "success", "data": user}