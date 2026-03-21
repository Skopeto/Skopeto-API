from abc import ABC, abstractmethod
import logging
from app.core.db_session import SessionManager
from app.core.dependencies import get_ssh_client
from app.modules.database_registry.application.service.database_connector import DatabaseConnector
from app.modules.database_registry.application.service.database_metrics_service import DatabaseMetricsServiceInterface
from app.modules.database_registry.application.use_case.collect_database_health import collect_databases_for_server_use_case
from app.modules.database_registry.infrastructure.sql_repository.sql_database_repository import SqlDatabaseRepository
from app.modules.docker_registry.application.service.docker_metrics_service import DockerMetricService
from app.modules.docker_registry.application.use_case.collect_container_metrics import collect_container_metrics_use_case
from app.modules.docker_registry.infrastructure.sql_repository.docker_repository import SqlDockerRepository
from app.modules.server_registry.application.service.server_metrics_service import ServerMetricsService
from app.modules.server_registry.application.use_case.collect_server_metrics import collect_server_metrics_use_case
from app.modules.server_registry.domain.entity.server import Server
from app.modules.server_registry.infrastructure.sql_repository.server_repository import SqlServerRepository

logger = logging.getLogger(__name__)


class MonitoringOrchestrationServiceInterface(ABC):
    @abstractmethod
    async def collect_single_server_monitoring(self, server: Server) -> dict | None:
        """Collect all monitoring data (health, containers, databases) for a single server."""
        pass


class MonitoringOrchestrationService(MonitoringOrchestrationServiceInterface):
    def __init__(
        self,
        database_metrics: DatabaseMetricsServiceInterface,
        connector: DatabaseConnector
    ):
        self.database_metrics = database_metrics
        self.connector = connector

    async def collect_single_server_monitoring(self, server: Server) -> dict | None:
        """Collect all monitoring data for a single server."""
        if server.id is None:
            return None

        check_results = []
        containers = []
        databases = []

        ssh_client = get_ssh_client()
        try:
            await ssh_client.connect_async(server)
            server_metrics = ServerMetricsService(ssh_client)
            docker_metrics = DockerMetricService(ssh_client)

            async with SessionManager.session_scope() as session:
                server_repository = SqlServerRepository(session)
                docker_repository = SqlDockerRepository(session)
                database_repository = SqlDatabaseRepository(session)

                try:
                    check_results = await collect_server_metrics_use_case(
                        server.id,
                        server_repository,
                        server_metrics
                    )

                    containers = await collect_container_metrics_use_case(
                        server,
                        check_results,
                        docker_repository,
                        docker_metrics
                    )

                    databases = await collect_databases_for_server_use_case(
                        server.id,
                        database_repository,
                        self.database_metrics,
                        self.connector,
                    )

                except Exception as e:
                    logger.error(f"Failed to collect server {server.id}: {e}")

        finally:
            await ssh_client.disconnect_async()

        return {
            "server": server,
            "check_results": check_results,
            "containers": containers,
            "databases": databases
        }
