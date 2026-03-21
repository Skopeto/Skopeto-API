from abc import ABC, abstractmethod
import logging
from app.core.dependencies import get_ssh_client
from app.modules.docker_registry.application.service.docker_metrics_service import DockerMetricService
from app.modules.docker_registry.application.use_case.collect_container_metrics import collect_container_metrics_use_case
from app.modules.docker_registry.application.use_case.get_containers import get_containers_use_case
from app.modules.docker_registry.domain.entity.docker_container import DockerContainer
from app.modules.docker_registry.domain.repository.docker_repository import DockerRepositoryInterface
from app.modules.server_registry.application.service.server_metrics_service import ServerMetricsService
from app.modules.server_registry.application.use_case.collect_server_metrics import collect_server_metrics_use_case
from app.modules.server_registry.application.use_case.get_server_health import get_server_health_use_case
from app.modules.server_registry.domain.entity.server import Server
from app.modules.server_registry.domain.entity.server_check_results import ServerCheckResults
from app.modules.server_registry.domain.repository.server_repository import ServerRepositoryInterface

logger = logging.getLogger(__name__)


class ContainerOrchestrationServiceInterface(ABC):
    @abstractmethod
    async def collect_server_containers(self, server_id: int) -> dict:
        """Collect server health and container metrics for a single server."""
        pass

    @abstractmethod
    async def get_all_servers_with_containers(self) -> list[dict]:
        """Get all servers with their containers and health status."""
        pass


class ContainerOrchestrationService(ContainerOrchestrationServiceInterface):
    def __init__(
        self,
        server_repo: ServerRepositoryInterface,
        docker_repo: DockerRepositoryInterface
    ):
        self.server_repo = server_repo
        self.docker_repo = docker_repo

    async def collect_server_containers(self, server_id: int) -> dict:
        """Collect server health and container metrics for a single server."""
        from app.core.Exception import ApplicationException

        server = await self.server_repo.get_server(server_id)
        if not server:
            raise ApplicationException(f"Server {server_id} not found")

        ssh_client = get_ssh_client()
        try:
            await ssh_client.connect_async(server)
            server_metrics = ServerMetricsService(ssh_client)
            docker_metrics = DockerMetricService(ssh_client)

            check_results = await collect_server_metrics_use_case(
                server_id,
                self.server_repo,
                server_metrics
            )

            containers = await collect_container_metrics_use_case(
                server,
                check_results,
                self.docker_repo,
                docker_metrics
            )

            return {
                "server": server,
                "check_results": check_results,
                "containers": containers
            }
        finally:
            await ssh_client.disconnect_async()

    async def get_all_servers_with_containers(self) -> list[dict]:
        """Get all servers with their containers and health status."""
        results = []
        servers = await self.server_repo.get_all_servers()

        for server in servers:
            if server.id is None:
                continue

            ssh_client = get_ssh_client()
            try:
                await ssh_client.connect_async(server)
                server_metrics = ServerMetricsService(ssh_client)
                check_results = await get_server_health_use_case(
                    server.id,
                    self.server_repo,
                    server_metrics
                )
            finally:
                await ssh_client.disconnect_async()

            containers = await get_containers_use_case(server.id, self.docker_repo)

            results.append({
                "server": server,
                "check_results": check_results,
                "containers": containers
            })

        return results
