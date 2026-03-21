import logging

from app.core.Exception import ApplicationException
from app.modules.server_health_ckeck.application.request.update_server_check_request import UpdateServerCheckRequest
from app.modules.server_health_ckeck.domain.entity.heallth_check import ServerCheck
from app.modules.server_health_ckeck.domain.repository.server_check_repository_interface import ServerCheckRepositoryInterface

logger = logging.getLogger(__name__)


async def update_server_check_use_case(
    health_check_id: int,
    request: UpdateServerCheckRequest,
    repository: ServerCheckRepositoryInterface
) -> ServerCheck:
    existing = await repository.get_server_check(health_check_id)
    if not existing:
        raise ApplicationException(f"Server check {health_check_id} not found")

    server_check = ServerCheck(
        health_check_id=health_check_id,
        name=request.name if request.name is not None else existing.name,
        command=request.command if request.command is not None else existing.command,
        threshold=request.threshold if request.threshold is not None else existing.threshold,
        operator=request.operator if request.operator is not None else existing.operator,
        unit=request.unit if request.unit is not None else existing.unit,
        check_status=request.check_status if request.check_status is not None else existing.check_status
    )

    return await repository.update_server_check(server_check)
