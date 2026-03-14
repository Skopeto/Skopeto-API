from fastapi import APIRouter, Depends
import logging
from app.modules.server_health_ckeck.application.request.register_server_check_request import RegisterServerCheckRequest
from app.modules.server_health_ckeck.application.use_case.register_server_check import register_server_check
from app.modules.server_health_ckeck.domain.repository.server_check_repository_interface import ServerCheckRepositoryInterface
from app.modules.auth.domain.entity.user import User
from app.core.security import get_current_user
from app.modules.server_health_ckeck.infrastructure.dependencies.dependencies import get_server_check_repository

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/server-checks", tags=["Server Checks"])

@router.post("", status_code=201)
async def create_server_check(
    request: RegisterServerCheckRequest,
    repository: ServerCheckRepositoryInterface = Depends(get_server_check_repository),
    current_user: User = Depends(get_current_user)
):
    """Register a new custom health check for servers."""
    server_check = await register_server_check(request, repository)
    return {"status": "success", "data": server_check}


@router.get("")
async def list_server_checks(
    current_user: User = Depends(get_current_user),
    repository: ServerCheckRepositoryInterface = Depends(get_server_check_repository),
):
    """Get all registered server health checks."""
    checks = await repository.get_server_checks()
    return {"status": "success", "data": checks}
