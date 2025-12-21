from fastapi import APIRouter, Depends
from app.modules.auth.application.request.register_user_request import RegisterUserRequest
from app.modules.auth.application.use_case.register_user_use_case import register_user_use_case
from app.modules.auth.domain.repository.user_repository import UserRepositoryInterface
from app.modules.auth.domain.entity.user import User
from app.core.security import get_current_user, get_user_repository

router = APIRouter()

@router.post("/auth/register")
def register(
    request: RegisterUserRequest,
    user_repository: UserRepositoryInterface = Depends(get_user_repository)
):
    user = register_user_use_case(request, user_repository)
    return user

@router.get("/auth/me")
async def get_me(current_user: User = Depends(get_current_user)):
    return current_user

@router.get("/protected-resource")
async def protected_route(current_user: User = Depends(get_current_user)):
    pass  # Your protected resource logic here