from fastapi import APIRouter, Depends
import logging
from app.core.Exception import ApplicationException
from app.modules.docker_registry.application.service.docker_metrics_service import DockerMetricService
from app.modules.docker_registry.application.use_case.collect_container_metrics import collect_container_metrics_use_case
from app.modules.docker_registry.application.use_case.get_containers import get_containers_use_case
from app.modules.docker_registry.domain.repository.docker_repository import DockerRepositoryInterface
from app.modules.docker_registry.infrastructure.dependencies.dependencies import get_docker_metrics_service, get_docker_repository
from app.modules.server_registry.application.service.server_metrics_service import ServerMetricsService
from app.modules.server_registry.application.use_case.collect_server_metrics import collect_server_metrics_use_case
from app.modules.server_registry.application.use_case.get_server_health import get_server_health_use_case
from app.modules.server_registry.domain.repository.server_repository import ServerRepositoryInterface
from app.modules.auth.domain.entity.user import User
from app.core.security import get_current_user
from app.modules.server_registry.infrastructure.dependencies.dependencies import get_server_metrics_service, get_server_repository

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/containers", tags=["Containers"])


@router.post("/collect/{server_id}")
async def collect_server_monitoring(
    server_id: int,
    current_user: User = Depends(get_current_user),
    server_repo: ServerRepositoryInterface = Depends(get_server_repository),
    docker_repo: DockerRepositoryInterface = Depends(get_docker_repository),
    server_metrics: ServerMetricsService = Depends(get_server_metrics_service),
    docker_metrics: DockerMetricService = Depends(get_docker_metrics_service)
):
    """
    Collects server health and container metrics for a single server.
    """
    server = await server_repo.get_server(server_id)
    if not server:
        raise ApplicationException(f"Server {server_id} not found")

    server_health = await collect_server_metrics_use_case(
        server_id,
        server_repo,
        server_metrics
    )

    containers = await collect_container_metrics_use_case(
        server_id,
        server,
        server_health,
        docker_repo,
        docker_metrics
    )

    return {
        "status": "success",
        "data": {
            "server": server,
            "current_health": server_health,
            "containers": containers
        }
    }


@router.get("/all")
async def get_all_servers_and_containers(
    current_user: User = Depends(get_current_user),
    server_repo: ServerRepositoryInterface = Depends(get_server_repository),
    docker_repo: DockerRepositoryInterface = Depends(get_docker_repository),
):
    """
    Gets all servers with their containers and health status.
    Used for: Container tab refresh
    """
    results = []
    servers = await server_repo.get_all_servers()
    for server in servers:
        if server.id is None:
            continue
        server_health = await get_server_health_use_case(server.id, server_repo)
        containers = await get_containers_use_case(server.id, docker_repo)

        results.append({
            "server": server,
            "server_health": server_health,
            "containers": containers
        })

    return {"status": "success", "data": results}
