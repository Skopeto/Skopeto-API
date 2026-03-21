from fastapi import APIRouter, Depends
import logging
from app.modules.docker_registry.application.service.container_orchestration_service import ContainerOrchestrationServiceInterface
from app.modules.docker_registry.infrastructure.dependencies.dependencies import get_container_orchestration_service
from app.modules.auth.domain.entity.user import User
from app.core.security import get_current_user

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/containers", tags=["Containers"])


@router.post("/{server_id}/collect")
async def collect_container_metrics(
    server_id: int,
    current_user: User = Depends(get_current_user),
    orchestration_service: ContainerOrchestrationServiceInterface = Depends(
        get_container_orchestration_service
    ),
):
    """
    Collects server health and container metrics for a single server.
    """
    result = await orchestration_service.collect_server_containers(server_id)
    return {"status": "success", "data": result}


@router.get("")
async def list_containers(
    current_user: User = Depends(get_current_user),
    orchestration_service: ContainerOrchestrationServiceInterface = Depends(
        get_container_orchestration_service
    ),
):
    """
    Gets all servers with their containers and health status.
    Used for: Container tab refresh
    """
    results = await orchestration_service.get_all_servers_with_containers()
    return {"status": "success", "data": results}
