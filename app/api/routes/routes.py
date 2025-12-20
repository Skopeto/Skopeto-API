from fastapi import APIRouter
from app.modules.auth.application.request.register_user_request import RegisterUserRequest
from app.modules.auth.application.use_case.register_user_use_case import register_user_use_case
from app.modules.auth.domain.repository.user_repository import UserRepositoryInterface

router = APIRouter()

@router.post("/auth/register")
def register(request: RegisterUserRequest, user_repository: UserRepositoryInterface):
    user = register_user_use_case(request, user_repository)
    return user

