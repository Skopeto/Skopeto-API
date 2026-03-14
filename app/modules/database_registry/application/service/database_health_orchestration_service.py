from abc import ABC, abstractmethod
from pydantic import BaseModel
from app.modules.database_registry.application.service.database_connector import DatabaseConnector
from app.modules.database_registry.application.service.database_metrics_service import DatabaseMetricsServiceInterface
from app.modules.database_registry.application.use_case.collect_database_health import collect_databases_for_server_use_case, DatabaseWithHealth
from app.modules.database_registry.domain.repository.database_repository import DatabaseRepositoryInterface
from app.modules.server_registry.application.service.server_metrics_service import ServerMetricsServiceInterface
from app.modules.server_registry.application.use_case.collect_server_metrics import collect_server_metrics_use_case
from app.modules.server_registry.domain.entity.server import Server
from app.modules.server_registry.domain.entity.server_health import ServerHealth
from app.modules.server_registry.domain.repository.server_repository import ServerRepositoryInterface


class ServerAndDatabaseHealthResponse(BaseModel):
    server: Server
    current_health: ServerHealth
    databases: list[DatabaseWithHealth]


class DatabaseHealthOrchestrationServiceInterface(ABC):
    @abstractmethod
    async def collect_server_with_databases_health(self, server_id: int) -> ServerAndDatabaseHealthResponse:
        """Collect server health and all database health for a specific server."""
        pass

    @abstractmethod
    async def collect_all_servers_with_databases_health(self) -> list[ServerAndDatabaseHealthResponse]:
        """Collect server health and database health for all servers."""
        pass


class DatabaseHealthOrchestrationService(DatabaseHealthOrchestrationServiceInterface):
    def __init__(
        self,
        server_repo: ServerRepositoryInterface,
        database_repo: DatabaseRepositoryInterface,
        server_metrics: ServerMetricsServiceInterface,
        database_metrics: DatabaseMetricsServiceInterface,
        connector: DatabaseConnector
    ):
        self.server_repo = server_repo
        self.database_repo = database_repo
        self.server_metrics = server_metrics
        self.database_metrics = database_metrics
        self.connector = connector

    async def collect_server_with_databases_health(self, server_id: int) -> ServerAndDatabaseHealthResponse:
        """Collect server health and all database health for a specific server."""
        server = await self.server_repo.get_server(server_id)

        if server is None or server.id is None:
            raise ValueError(f"Server {server_id} not found")

        server_health = await collect_server_metrics_use_case(
            server.id,
            self.server_repo,
            self.server_metrics
        )

        databases = await collect_databases_for_server_use_case(
            server.id,
            self.database_repo,
            self.database_metrics,
            self.connector,
        )

        return ServerAndDatabaseHealthResponse(
            server=server,
            current_health=server_health,
            databases=databases,
        )

    async def collect_all_servers_with_databases_health(self) -> list[ServerAndDatabaseHealthResponse]:
        """Collect server health and database health for all servers."""
        results = []
        servers = await self.server_repo.get_all_servers()

        for server in servers:
            if server.id is None:
                continue

            server_health = await collect_server_metrics_use_case(
                server.id,
                self.server_repo,
                self.server_metrics
            )

            databases = await collect_databases_for_server_use_case(
                server.id,
                self.database_repo,
                self.database_metrics,
                self.connector,
            )

            results.append(
                ServerAndDatabaseHealthResponse(
                    server=server,
                    current_health=server_health,
                    databases=databases,
                )
            )

        return results
