from fastapi import APIRouter, Depends, HTTPException
from app.core.Exception import SecurityException
from app.modules.docker_registry.application.service.docker_metrics_service import DockerMetricService
from app.modules.docker_registry.domain.repository.docker_repository import DockerRepositoryInterface
from app.modules.docker_registry.infrastructure.dependencies.dependencies import get_docker_metrics_service, get_docker_repository
from app.modules.server_registry.application.request.register_server_location_request import RegisterServerLocationRequest
from app.modules.server_registry.application.service.server_metrics_service import ServerMetricsService
from app.modules.server_registry.application.use_case.collect_all_monitoring import collect_all_servers_monitoring_use_case
from app.modules.server_registry.application.use_case.get_servers import get_servers_use_case
from app.modules.server_registry.application.use_case.register_server import register_server_use_case
from app.modules.server_registry.application.use_case.collect_server_health import collect_server_health_use_case
from app.modules.server_registry.domain.repository.server_repository import ServerRepositoryInterface
from app.modules.auth.domain.entity.user import User
from app.core.security import get_current_user
from app.modules.server_registry.infrastructure.dependencies.dependencies import get_server_metrics_service, get_server_repository, get_ssh_client

router = APIRouter(prefix="/servers", tags=["Servers"])

@router.post("/register", status_code=201)
async def register_server(
    request: RegisterServerLocationRequest,
    server_repository: ServerRepositoryInterface = Depends(get_server_repository),
    current_user: User = Depends(get_current_user)
):
    if request.registrator_id != current_user.id:
        raise SecurityException("Cannot register server for another user")

    server = await register_server_use_case(request, server_repository)
    return {"status": "success", "data": server}

@router.get("/server-health/{server_id}")
async def get_server_health(
    server_id: int,
    current_user: User = Depends(get_current_user),
    server_repository: ServerRepositoryInterface = Depends(get_server_repository),
    server_metrics: ServerMetricsService = Depends(get_server_metrics_service)
):
    server_health = await collect_server_health_use_case(server_id, server_repository, server_metrics)
    return {"status": "success", "data": server_health}

@router.get("/all-servers")
async def get_servers(
    current_user: User = Depends(get_current_user),
    server_repository: ServerRepositoryInterface = Depends(get_server_repository),
):
    servers = await get_servers_use_case(server_repository)
    return {"status": "success", "data": servers}

@router.post("/monitoring/collect-all")
async def collect_all_monitoring(
    server_repo: ServerRepositoryInterface = Depends(get_server_repository),
    docker_repo: DockerRepositoryInterface = Depends(get_docker_repository),
    server_metrics: ServerMetricsService = Depends(get_server_metrics_service),
    docker_metrics: DockerMetricService = Depends(get_docker_metrics_service)
):
    results = await collect_all_servers_monitoring_use_case(
        server_repo,
        docker_repo,
        server_metrics,
        docker_metrics
    )
    return {"status": "success", "data": results}


