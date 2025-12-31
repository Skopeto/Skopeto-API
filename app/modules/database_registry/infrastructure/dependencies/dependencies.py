from app.core.db_session import SessionDep
from app.modules.database_registry.application.service.database_metrics_service import (
    DatabaseMetricsService,
    DatabaseMetricsServiceInterface,
)
from app.modules.database_registry.application.service.database_connector import (
    DatabaseConnector,
)
from app.modules.database_registry.domain.repository.database_repository import (
    DatabaseRepositoryInterface,
)
from app.modules.database_registry.infrastructure.sql_repository.sql_database_repository import (
    SqlDatabaseRepository,
)


def get_database_metrics_service() -> DatabaseMetricsServiceInterface:
    return DatabaseMetricsService()


def get_database_connector() -> DatabaseConnector:
    return DatabaseConnector()


def get_database_repository(session: SessionDep) -> DatabaseRepositoryInterface:
    return SqlDatabaseRepository(session)
