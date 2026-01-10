from fastapi import APIRouter, Depends
import logging
from pydantic import BaseModel
from app.modules.database_registry.application.request.register_database_request import (
    RegisterDatabaseRequest,
)
from app.modules.database_registry.application.request.update_database_request import (
    UpdateDatabaseRequest,
)
from app.modules.database_registry.application.service.database_connector import (
    DatabaseConnector,
)
from app.modules.database_registry.application.service.database_metrics_service import (
    DatabaseMetricsServiceInterface,
)
from app.modules.database_registry.application.use_case.collect_database_health import (
    collect_databases_for_server_use_case,
    DatabaseWithHealth,
)
from app.modules.database_registry.application.use_case.delete_database import (
    delete_database_use_case,
)
from app.modules.database_registry.application.use_case.edit_database import (
    edit_database_use_case,
)
from app.modules.database_registry.application.use_case.register_database import (
    register_database_use_case,
)
from app.modules.database_registry.domain.repository.database_repository import (
    DatabaseRepositoryInterface,
)
from app.modules.database_registry.infrastructure.dependencies.dependencies import (
    get_database_connector,
    get_database_metrics_service,
    get_database_repository,
)
from app.modules.server_registry.application.service.server_metrics_service import (
    ServerMetricsServiceInterface,
)
from app.modules.server_registry.application.use_case.collect_server_metrics import collect_server_metrics_use_case
from app.modules.server_registry.domain.entity.server import Server
from app.modules.server_registry.domain.entity.server_health import ServerHealth
from app.modules.server_registry.domain.repository.server_repository import (
    ServerRepositoryInterface,
)
from app.modules.auth.domain.entity.user import User
from app.core.security import get_current_user
from app.modules.server_registry.infrastructure.dependencies.dependencies import (
    get_server_metrics_service,
    get_server_repository,
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/databases", tags=["Databases"])


class ServerAndDatabaseHealthResponse(BaseModel):
    server: Server
    current_health: ServerHealth
    databases: list[DatabaseWithHealth]

@router.get("/health")
async def get_databases_health(
    database_metrics: DatabaseMetricsServiceInterface = Depends(
        get_database_metrics_service
    ),
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
        server_health = await collect_server_metrics_use_case(
            server.id,
            server_repo,
            server_metrics
        )

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

@router.get("/health/{server_id}")
async def get_database_health(
    server_id: int,
    database_metrics: DatabaseMetricsServiceInterface = Depends(
        get_database_metrics_service
    ),
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
    server = await server_repo.get_server(server_id)
    if server is None or server.id is None:
        return {"status": "error", "data": results}
    # Get server health (server module)
    server_health = await collect_server_metrics_use_case(
        server.id,
        server_repo,
        server_metrics
    )

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

@router.post("")
async def create_database(
    request: RegisterDatabaseRequest,
    database_repo: DatabaseRepositoryInterface = Depends(get_database_repository),
    current_user: User = Depends(get_current_user),
):
    """Register a new database for monitoring."""
    registered_db = await register_database_use_case(request, database_repo)
    return {"status": "success", "data": registered_db}


@router.patch("/{database_id}")
async def update_database(
    database_id: int,
    request: UpdateDatabaseRequest,
    database_repo: DatabaseRepositoryInterface = Depends(get_database_repository),
    current_user: User = Depends(get_current_user),
):
    """Update database configuration."""
    database = await edit_database_use_case(database_id, request, database_repo)
    return {"status": "success", "data": database}


@router.delete("/{database_id}")
async def delete_database(
    database_id: int,
    database_repo: DatabaseRepositoryInterface = Depends(get_database_repository),
    current_user: User = Depends(get_current_user),
):
    """Delete a database from monitoring."""
    await delete_database_use_case(database_id, database_repo)
    return {"status": "success", "data": f"Database {database_id} deleted successfully"}
