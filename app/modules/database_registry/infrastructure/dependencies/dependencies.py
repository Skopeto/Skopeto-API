from fastapi import Depends
from app.core.db_session import SessionDep
from app.modules.database_registry.application.service.database_health_orchestration_service import (
    DatabaseHealthOrchestrationService,
    DatabaseHealthOrchestrationServiceInterface,
)
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
from app.modules.server_registry.domain.repository.server_repository import ServerRepositoryInterface
from app.modules.server_registry.infrastructure.dependencies.dependencies import get_server_repository


def get_database_metrics_service() -> DatabaseMetricsServiceInterface:
    return DatabaseMetricsService()


def get_database_connector() -> DatabaseConnector:
    return DatabaseConnector()


def get_database_repository(session: SessionDep) -> DatabaseRepositoryInterface:
    return SqlDatabaseRepository(session)


def get_database_health_orchestration_service(
    server_repo: ServerRepositoryInterface = Depends(get_server_repository),
    database_repo: DatabaseRepositoryInterface = Depends(get_database_repository),
    database_metrics: DatabaseMetricsServiceInterface = Depends(get_database_metrics_service),
    connector: DatabaseConnector = Depends(get_database_connector)
) -> DatabaseHealthOrchestrationServiceInterface:
    return DatabaseHealthOrchestrationService(
        server_repo=server_repo,
        database_repo=database_repo,
        database_metrics=database_metrics,
        connector=connector
    )
