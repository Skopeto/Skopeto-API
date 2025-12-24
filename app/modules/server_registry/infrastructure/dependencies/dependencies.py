from app.core.dependencies import get_ssh_client
from app.modules.server_registry.application.service.server_metrics_service import ServerMetricsService
from app.modules.server_registry.domain.repository.server_repository import ServerRepositoryInterface
from app.modules.server_registry.infrastructure.sql_repository.server_repository import SqlServerRepository
from app.core.db_session import SessionDep

def get_server_repository(session: SessionDep) -> ServerRepositoryInterface:
    return SqlServerRepository(session)

def get_server_metrics_service() -> ServerMetricsService:
    return ServerMetricsService(get_ssh_client())