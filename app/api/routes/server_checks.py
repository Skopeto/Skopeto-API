from fastapi import APIRouter, Depends, HTTPException
import logging
from app.modules.server_health_ckeck.application.request.register_server_check_request import RegisterServerCheckRequest
from app.modules.server_health_ckeck.application.request.update_server_check_request import UpdateServerCheckRequest
from app.modules.server_health_ckeck.application.use_case.register_server_check import register_server_check
from app.modules.server_health_ckeck.domain.entity.heallth_check import ServerCheck
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


@router.get("/{health_check_id}")
async def get_server_check(
    health_check_id: int,
    current_user: User = Depends(get_current_user),
    repository: ServerCheckRepositoryInterface = Depends(get_server_check_repository),
):
    """Get a specific server health check by ID."""
    check = await repository.get_server_check(health_check_id)
    if not check:
        raise HTTPException(status_code=404, detail=f"Server check {health_check_id} not found")
    return {"status": "success", "data": check}


@router.put("/{health_check_id}")
async def update_server_check(
    health_check_id: int,
    request: UpdateServerCheckRequest,
    current_user: User = Depends(get_current_user),
    repository: ServerCheckRepositoryInterface = Depends(get_server_check_repository),
):
    """Update an existing server health check."""
    existing = await repository.get_server_check(health_check_id)
    if not existing:
        raise HTTPException(status_code=404, detail=f"Server check {health_check_id} not found")

    server_check = ServerCheck(
        health_check_id=health_check_id,
        name=request.name if request.name is not None else existing.name,
        command=request.command if request.command is not None else existing.command,
        threshold=request.threshold if request.threshold is not None else existing.threshold,
        operator=request.operator if request.operator is not None else existing.operator,
        unit=request.unit if request.unit is not None else existing.unit,
        check_status=request.check_status if request.check_status is not None else existing.check_status
    )
    updated = await repository.update_server_check(server_check)
    return {"status": "success", "data": updated}


@router.delete("/{health_check_id}", status_code=204)
async def delete_server_check(
    health_check_id: int,
    current_user: User = Depends(get_current_user),
    repository: ServerCheckRepositoryInterface = Depends(get_server_check_repository),
):
    """Delete a server health check."""
    existing = await repository.get_server_check(health_check_id)
    if not existing:
        raise HTTPException(status_code=404, detail=f"Server check {health_check_id} not found")

    await repository.delete_server_check(health_check_id)
    return None
