from fastapi import APIRouter, Depends
import logging
from app.core.Exception import SecurityException
from app.modules.server_registry.application.request.register_server_location_request import RegisterServerLocationRequest
from app.modules.server_registry.application.request.update_server_request import UpdateServerRequest
from app.modules.server_registry.application.use_case.delete_server import delete_server_use_case
from app.modules.server_registry.application.use_case.edit_server import edit_server_use_case
from app.modules.server_registry.application.use_case.get_servers import get_servers_use_case
from app.modules.server_registry.application.use_case.register_server import register_server_use_case
from app.modules.server_registry.domain.repository.server_repository import ServerRepositoryInterface
from app.modules.auth.domain.entity.user import User
from app.core.security import get_current_user
from app.modules.server_registry.infrastructure.dependencies.dependencies import get_server_repository

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/servers", tags=["Servers"])

@router.post("/register", status_code=201)
async def register_server(
    request: RegisterServerLocationRequest,
    server_repository: ServerRepositoryInterface = Depends(get_server_repository),
    current_user: User = Depends(get_current_user)
):
    """Register a new server for monitoring."""
    if request.registrator_id != current_user.id:
        raise SecurityException("Cannot register server for another user")

    server = await register_server_use_case(request, server_repository)
    return {"status": "success", "data": server}


@router.get("/all-servers")
async def get_servers(
    current_user: User = Depends(get_current_user),
    server_repository: ServerRepositoryInterface = Depends(get_server_repository),
):
    servers = await get_servers_use_case(server_repository)
    
    return {"status": "success", "data": servers}


@router.patch('/edit/{server_id}')
async def edit_server(
    server_id: int,
    request: UpdateServerRequest,
    current_user: User = Depends(get_current_user),
    server_repo: ServerRepositoryInterface = Depends(get_server_repository),
):
    """Update server details."""
    result = await edit_server_use_case(
        server_id,
        request,
        server_repo
    )
    return {"status": "success", "data": result}


@router.delete('/delete/{server_id}')
async def delete_server(
    server_id: int,
    current_user: User = Depends(get_current_user),
    server_repo: ServerRepositoryInterface = Depends(get_server_repository),
):
    """Delete a server."""
    await delete_server_use_case(
        server_id,
        server_repo
    )
    return {"status": "success"}