from fastapi import APIRouter, Depends
from app.modules.auth.application.request.login_request import LoginRequest
from app.modules.auth.application.request.register_user_request import RegisterUserRequest
from app.modules.auth.application.use_case.user_login_use_case import user_login_use_case
from app.modules.auth.application.use_case.register_user_use_case import register_user_use_case
from app.modules.auth.domain.repository.user_repository import UserRepositoryInterface
from app.core.security import get_user_repository

router = APIRouter()

@router.post("/auth/register", status_code=201)
async def register(
    request: RegisterUserRequest,
    user_repository: UserRepositoryInterface = Depends(get_user_repository)
):
    user = await register_user_use_case(request, user_repository)
    return {"status": "success", "data": user}

@router.post("/auth/login")
async def login(
    request: LoginRequest,
    user_repository: UserRepositoryInterface = Depends(get_user_repository)
):
    token = await user_login_use_case(request, user_repository)
    return {"status": "success", "data": token}
