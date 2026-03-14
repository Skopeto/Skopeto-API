from fastapi import APIRouter, Depends
import logging
from app.modules.auth.domain.entity.user import User
from app.core.security import get_current_user
from app.modules.database_registry.application.request.register_database_request import (
    RegisterDatabaseRequest,
)
from app.modules.database_registry.application.request.update_database_request import (
    UpdateDatabaseRequest,
)
from app.modules.database_registry.application.service.database_health_orchestration_service import (
    DatabaseHealthOrchestrationServiceInterface,
)
from app.modules.database_registry.application.use_case.delete_database import (
    delete_database_use_case,
)
from app.modules.database_registry.application.use_case.edit_database import (
    edit_database_use_case,
)
from app.modules.database_registry.application.use_case.get_all_databases_with_health import (
    get_all_databases_with_health_use_case,
)
from app.modules.database_registry.application.use_case.get_server_databases_with_health import (
    get_server_databases_with_health_use_case,
)
from app.modules.database_registry.application.use_case.register_database import (
    register_database_use_case,
)
from app.modules.database_registry.domain.repository.database_repository import (
    DatabaseRepositoryInterface,
)
from app.modules.database_registry.infrastructure.dependencies.dependencies import (
    get_database_health_orchestration_service,
    get_database_repository,
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/databases", tags=["Databases"])


@router.get("/health")
async def get_databases_health(
    current_user: User = Depends(get_current_user),
    orchestration_service: DatabaseHealthOrchestrationServiceInterface = Depends(
        get_database_health_orchestration_service
    ),
):
    """
    Collects database health for all servers and their databases.
    Used for: Database tab refresh
    """
    results = await get_all_databases_with_health_use_case(orchestration_service)
    return {"status": "success", "data": results}

@router.get("/health/{server_id}")
async def get_database_health(
    server_id: int,
    current_user: User = Depends(get_current_user),
    orchestration_service: DatabaseHealthOrchestrationServiceInterface = Depends(
        get_database_health_orchestration_service
    ),
):
    """
    Collects database health for a specific server and its databases.
    Used for: Database tab refresh (single server)
    """
    result = await get_server_databases_with_health_use_case(server_id, orchestration_service)
    return {"status": "success", "data": result}

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
