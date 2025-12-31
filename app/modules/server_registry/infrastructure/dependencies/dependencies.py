from fastapi import Depends
from app.core.dependencies import get_ssh_client
from app.core.ssh_client import SSHClientInterface
from app.modules.server_registry.application.service.server_metrics_service import ServerMetricsService, ServerMetricsServiceInterface
from app.modules.server_registry.domain.repository.server_repository import ServerRepositoryInterface
from app.modules.server_registry.infrastructure.sql_repository.server_repository import SqlServerRepository
from app.core.db_session import SessionDep

def get_server_repository(session: SessionDep) -> ServerRepositoryInterface:
    return SqlServerRepository(session)

def get_server_metrics_service(
    ssh_client: SSHClientInterface = Depends(get_ssh_client),
) -> ServerMetricsServiceInterface:
    return ServerMetricsService(ssh_client)