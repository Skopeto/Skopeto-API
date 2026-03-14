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


@router.patch('/{check_id}')
async def update_server_check(
    check_id: int,
    request: RegisterServerCheckRequest,
    current_user: User = Depends(get_current_user),
    repository: ServerCheckRepositoryInterface = Depends(get_server_check_repository),
):
    """Update server health check details."""
    # Note: You'll need to implement an update use case
    # This is a placeholder following the pattern
    from app.modules.server_health_ckeck.domain.entity.heallth_check import ServerCheck

    server_check = ServerCheck(
        health_check_id=check_id,
        name=request.name,
        command=request.command,
        threshold=request.threshold,
        operator=request.operator,
        check_status=request.check_status if hasattr(request, 'check_status') else None
    )

    await repository.update_server_check(server_check)
    return {"status": "success", "data": server_check}


@router.delete('/{check_id}')
async def delete_server_check(
    check_id: int,
    current_user: User = Depends(get_current_user),
    repository: ServerCheckRepositoryInterface = Depends(get_server_check_repository),
):
    """Delete a server health check."""
    await repository.delete_server_check(str(check_id))
    return {"status": "success"}
