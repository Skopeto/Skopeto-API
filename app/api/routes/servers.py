from fastapi import APIRouter, Depends, HTTPException
from app.modules.server_registry.application.request.register_server_location_request import RegisterServerLocationRequest
from app.modules.server_registry.application.service.server_metrics_service import ServerMetricsService
from app.modules.server_registry.application.use_case.register_server import register_server_use_case
from app.modules.server_registry.application.use_case.collect_server_health import collect_server_health_use_case
from app.modules.server_registry.domain.repository.server_repository import ServerRepositoryInterface
from app.modules.auth.domain.entity.user import User
from app.core.security import get_current_user
from app.modules.server_registry.infrastructure.dependencies.dependencies import get_server_repository, get_ssh_client

router = APIRouter(prefix="/servers", tags=["Servers"])

@router.post("/register")
def register_server(
    request: RegisterServerLocationRequest,
    current_user: User = Depends(get_current_user),
    server_repository: ServerRepositoryInterface = Depends(get_server_repository)
):
    if request.registrator_id != current_user.id:
        raise HTTPException(status_code=403, detail="Cannot register server for another user")
    
    server =  register_server_use_case(request, server_repository)
    return server

@router.get("/server-health/{server_id}")
async def get_server_health(
    server_id: int,
    current_user: User = Depends(get_current_user),
    server_repository: ServerRepositoryInterface = Depends(get_server_repository),
    ssh_client: ServerMetricsService = Depends(get_ssh_client)
):
    
    server_health = await collect_server_health_use_case(server_id, server_repository, ssh_client)
    return server_health

