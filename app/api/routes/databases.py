from fastapi import APIRouter, Depends
import logging
from pydantic import BaseModel
from app.modules.database_registry.application.request.register_database_request import RegisterDatabaseRequest
from app.modules.database_registry.application.service.database_connector import DatabaseConnector
from app.modules.database_registry.application.service.database_metrics_service import DatabaseMetricsServiceInterface
from app.modules.database_registry.application.use_case.collect_database_health import collect_databases_for_server_use_case, DatabaseWithHealth
from app.modules.database_registry.application.use_case.register_database import register_database_use_case
from app.modules.database_registry.domain.repository.database_repository import DatabaseRepositoryInterface
from app.modules.database_registry.infrastructure.dependencies.dependencies import get_database_connector, get_database_metrics_service, get_database_repository
from app.modules.server_registry.application.service.server_metrics_service import ServerMetricsServiceInterface
from app.modules.server_registry.domain.entity.server import Server
from app.modules.server_registry.domain.entity.server_health import ServerHealth
from app.modules.server_registry.domain.repository.server_repository import ServerRepositoryInterface
from app.modules.auth.domain.entity.user import User
from app.core.security import get_current_user
from app.modules.server_registry.infrastructure.dependencies.dependencies import get_server_metrics_service, get_server_repository

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/databases", tags=["Databases"])


class ServerAndDatabaseHealthResponse(BaseModel):
    server: Server
    current_health: ServerHealth
    databases: list[DatabaseWithHealth]


@router.get('/collect/all')
async def get_databases(
    database_metrics: DatabaseMetricsServiceInterface = Depends(get_database_metrics_service),
    connector: DatabaseConnector = Depends(get_database_connector),
    database_repo: DatabaseRepositoryInterface = Depends(get_database_repository),
    server_repo: ServerRepositoryInterface = Depends(get_server_repository),
    server_metrics: ServerMetricsServiceInterface = Depends(get_server_metrics_service),
    current_user: User = Depends(get_current_user),
):
    """
    Collects database health for all servers and their databases.
    Used for: Database tab refresh
    """
    results = []
    servers = await server_repo.get_all_servers()

    for server in servers:
        if server.id is None:
            continue

        # Get server health (server module)
        server_health_dict = await server_metrics.get_server_metrics(server)
        server_health = ServerHealth(**server_health_dict)

        # Get databases with health (database module - pass only server_id)
        databases = await collect_databases_for_server_use_case(
            server.id,
            database_repo,
            database_metrics,
            connector,
        )

        # Combine results (orchestration)
        results.append(
            ServerAndDatabaseHealthResponse(
                server=server,
                current_health=server_health,
                databases=databases,
            )
        )

    return {"status": "success", "data": results}


@router.post('/register')
async def register_database(
    request: RegisterDatabaseRequest,
    database_repo: DatabaseRepositoryInterface = Depends(get_database_repository),
    current_user: User = Depends(get_current_user),
):
    registered_db = await register_database_use_case(
        request,
        database_repo
    )
    return {"status": "success", "data": registered_db}