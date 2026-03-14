from fastapi import APIRouter, Depends
import logging
from app.modules.auth.domain.entity.user import User
from app.core.security import get_current_user
from app.modules.monitoring.application.service.monitoring_orchestration_service import MonitoringOrchestrationServiceInterface
from app.modules.monitoring.application.use_case.collect_all_monitoring import collect_all_monitoring_use_case
from app.modules.monitoring.infrastructure.dependencies.dependencies import get_monitoring_orchestration_service
from app.modules.server_registry.domain.repository.server_repository import ServerRepositoryInterface
from app.modules.server_registry.infrastructure.dependencies.dependencies import get_server_repository

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/monitoring", tags=["Monitoring"])

@router.post("/collect")
async def collect_monitoring(
    current_user: User = Depends(get_current_user),
    server_repository: ServerRepositoryInterface = Depends(get_server_repository),
    monitoring_service: MonitoringOrchestrationServiceInterface = Depends(get_monitoring_orchestration_service),
):
    """
    Collects complete monitoring data for all servers.
    Includes: server health, containers, and databases.
    Used for: Dashboard full refresh
    """
    results = await collect_all_monitoring_use_case(server_repository, monitoring_service)
    return {"status": "success", "data": results}
