from fastapi import APIRouter, Depends
from app.core.Exception import SecurityException
from app.modules.docker_registry.application.service.docker_metrics_service import DockerMetricService
from app.modules.docker_registry.domain.repository.docker_repository import DockerRepositoryInterface
from app.modules.docker_registry.infrastructure.dependencies.dependencies import get_docker_metrics_service, get_docker_repository
from app.modules.server_registry.application.request.register_server_location_request import RegisterServerLocationRequest
from app.modules.server_registry.application.service.server_metrics_service import ServerMetricsService
from app.modules.server_registry.application.use_case.collect_and_persist_all_monitoring import collect_and_persist_all_monitoring_use_case
from app.modules.server_registry.application.use_case.get_servers import get_servers_use_case
from app.modules.server_registry.application.use_case.get_servers_with_containers import get_servers_with_containers_use_case
from app.modules.server_registry.application.use_case.register_server import register_server_use_case
from app.modules.server_registry.application.use_case.collect_and_persist_single_monitoring import collect_and_persist_single_monitoring_use_case
from app.modules.server_registry.domain.repository.server_repository import ServerRepositoryInterface
from app.modules.auth.domain.entity.user import User
from app.core.security import get_current_user
from app.modules.server_registry.infrastructure.dependencies.dependencies import get_server_metrics_service, get_server_repository

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

@router.get("/monitoting/{server_id}")
async def get_server_health(
    server_id: int,
    current_user: User = Depends(get_current_user),
    server_repository: ServerRepositoryInterface = Depends(get_server_repository),
    docker_repository: DockerRepositoryInterface = Depends(get_docker_repository),
    server_metrics: ServerMetricsService = Depends(get_server_metrics_service),
    docker_metrics: DockerMetricService = Depends(get_docker_metrics_service)
):
    results = await collect_and_persist_single_monitoring_use_case(
        server_id,
        server_repository,
        docker_repository,
        server_metrics,
        docker_metrics
    )
    return {"status": "success", "data": results}

@router.get("/all-servers")
async def get_servers(
    current_user: User = Depends(get_current_user),
    server_repository: ServerRepositoryInterface = Depends(get_server_repository),
):
    servers = await get_servers_use_case(server_repository)
    return {"status": "success", "data": servers}

@router.get("/monitoring/collect-all")
async def collect_all_monitoring(
    current_user: User = Depends(get_current_user),
    server_repository: ServerRepositoryInterface = Depends(get_server_repository),
    docker_repository: DockerRepositoryInterface = Depends(get_docker_repository),
    server_metrics: ServerMetricsService = Depends(get_server_metrics_service),
    docker_metrics: DockerMetricService = Depends(get_docker_metrics_service)
):
    results = await collect_and_persist_all_monitoring_use_case(
        server_repository,
        docker_repository,
        server_metrics,
        docker_metrics
    )
    return {"status": "success", "data": results}

@router.get("/containers/all")
async def get_all_servers_and_containers(
    current_user: User = Depends(get_current_user),
    server_repo: ServerRepositoryInterface = Depends(get_server_repository),
    docker_repo: DockerRepositoryInterface = Depends(get_docker_repository),
):
    results = await get_servers_with_containers_use_case(
        server_repo,
        docker_repo,
    )
    return {"status": "success", "data": results}
