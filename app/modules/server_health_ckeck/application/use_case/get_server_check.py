import logging

from app.core.Exception import ApplicationException
from app.modules.server_health_ckeck.domain.entity.heallth_check import ServerCheck
from app.modules.server_health_ckeck.domain.repository.server_check_repository_interface import ServerCheckRepositoryInterface

logger = logging.getLogger(__name__)


async def get_server_check_use_case(
    health_check_id: int,
    repository: ServerCheckRepositoryInterface
) -> ServerCheck:
    check = await repository.get_server_check(health_check_id)
    if not check:
        raise ApplicationException(f"Server check {health_check_id} not found")
    return check
