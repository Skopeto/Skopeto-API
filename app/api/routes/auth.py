from fastapi import APIRouter, Depends
from app.modules.auth.application.request.register_user_request import RegisterUserRequest
from app.modules.auth.application.use_case.register_user_use_case import register_user_use_case
from app.modules.auth.domain.repository.user_repository import UserRepositoryInterface
from app.modules.auth.domain.entity.user import User
from app.core.security import get_current_user, get_user_repository
from app.modules.server_registry.application.request.register_server_location_request import RegisterServerLocationRequest
from app.modules.server_registry.application.use_case.register_server import register_server_use_case
from app.modules.server_registry.domain.repository.server_repository import ServerRepositoryInterface
from app.core.Exception import SecurityException
from app.modules.server_registry.infrastructure.dependencies.dependencies import get_server_repository

router = APIRouter()

@router.post("/auth/register")
def register(
    request: RegisterUserRequest,
    user_repository: UserRepositoryInterface = Depends(get_user_repository)
):
    user = register_user_use_case(request, user_repository)
    return {"status": "success", "data": user}

@router.get("/auth/me")
async def get_me(current_user: User = Depends(get_current_user)):
    return {"status": "success", "data": current_user}

@router.post("/servers/register")
def register_server(
    request: RegisterServerLocationRequest,
    server_repository: ServerRepositoryInterface = Depends(get_server_repository),
    current_user: User = Depends(get_current_user)
):
    if request.registrator_id != current_user.id:
        raise SecurityException("Cannot register server for another user")
    
    server = register_server_use_case(request, server_repository)
    return {"status": "success", "data": server}