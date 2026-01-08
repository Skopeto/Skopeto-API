from fastapi import APIRouter, Depends
import logging
import asyncio
from app.core.Exception import ApplicationException
from app.modules.database_registry.application.service.database_connector import DatabaseConnector
from app.modules.database_registry.application.service.database_metrics_service import DatabaseMetricsServiceInterface
from app.modules.database_registry.application.use_case.collect_database_health import collect_databases_for_server_use_case
from app.modules.database_registry.domain.repository.database_repository import DatabaseRepositoryInterface
from app.modules.database_registry.infrastructure.dependencies.dependencies import get_database_connector, get_database_metrics_service, get_database_repository
from app.modules.docker_registry.application.service.docker_metrics_service import DockerMetricService
from app.modules.docker_registry.application.use_case.collect_container_metrics import collect_container_metrics_use_case
from app.modules.docker_registry.domain.repository.docker_repository import DockerRepositoryInterface
from app.modules.docker_registry.infrastructure.dependencies.dependencies import get_docker_metrics_service, get_docker_repository
from app.modules.server_registry.application.service.server_metrics_service import ServerMetricsService
from app.modules.server_registry.application.use_case.collect_server_metrics import collect_server_metrics_use_case
from app.modules.server_registry.domain.entity.server import Server
from app.modules.server_registry.domain.repository.server_repository import ServerRepositoryInterface
from app.modules.auth.domain.entity.user import User
from app.core.security import get_current_user
from app.modules.server_registry.infrastructure.dependencies.dependencies import get_server_metrics_service, get_server_repository

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/monitoring", tags=["Monitoring"])


@router.post("/collect")
async def collect_monitoring(
    current_user: User = Depends(get_current_user),
    server_repository: ServerRepositoryInterface = Depends(get_server_repository),
    docker_repository: DockerRepositoryInterface = Depends(get_docker_repository),
    database_repository: DatabaseRepositoryInterface = Depends(get_database_repository),
    server_metrics: ServerMetricsService = Depends(get_server_metrics_service),
    docker_metrics: DockerMetricService = Depends(get_docker_metrics_service),
    database_metrics: DatabaseMetricsServiceInterface = Depends(get_database_metrics_service),
    connector: DatabaseConnector = Depends(get_database_connector),
):
    """
    Collects complete monitoring data for all servers.
    Includes: server health, containers, and databases.
    Used for: Dashboard full refresh
    """
    servers = await server_repository.get_all_servers()

    if not servers:
        raise ApplicationException("No servers found")

    async def collect_single_server(server: Server):
        if server.id is None:
            return None

        try:
            server_health = await collect_server_metrics_use_case(
                server.id,
                server_repository,
                server_metrics
            )

            containers = await collect_container_metrics_use_case(
                server.id,
                server,
                server_health,
                docker_repository,
                docker_metrics
            )

            databases = await collect_databases_for_server_use_case(
                server.id,
                database_repository,
                database_metrics,
                connector,
            )

            return {
                "server": server,
                "current_health": server_health,
                "containers": containers,
                "databases": databases
            }
        except Exception as e:
            logger.error(f"Failed to collect server {server.id}: {e}")
            return None

    results = await asyncio.gather(
        *[collect_single_server(server) for server in servers],
        return_exceptions=False
    )

    valid_results = [result for result in results if result is not None]

    return {"status": "success", "data": valid_results}
