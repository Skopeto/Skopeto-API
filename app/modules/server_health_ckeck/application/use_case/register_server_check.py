import logging

from app.modules.server_health_ckeck.application.request.register_server_check_request import RegisterServerCheckRequest
from app.modules.server_health_ckeck.domain.entity.heallth_check import ServerCheck
from app.modules.server_health_ckeck.domain.enum.health_check_status import HealthCheckStatus
from app.modules.server_health_ckeck.domain.repository.server_check_repository_interface import ServerCheckRepositoryInterface
from app.services.get_next_id import get_next_id

logger = logging.getLogger(__name__)

async def register_server_check(
    request: RegisterServerCheckRequest,
    repository: ServerCheckRepositoryInterface
)-> ServerCheck:

    id = await get_next_id(repository, "health_check_id_seq")
    if not id:
        raise Exception("Failed to get next id for health check")
    
    server_check = ServerCheck(
        health_check_id=id,
        name=request.name,
        command=request.command,
        threshold=request.threshold,
        operator=request.operator,
        check_status=HealthCheckStatus.ACTIVE
    )

    await repository.create_server_check(server_check)

    return server_check
