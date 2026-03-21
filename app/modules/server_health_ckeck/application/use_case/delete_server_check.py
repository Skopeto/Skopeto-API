import logging

from app.core.Exception import ApplicationException
from app.modules.server_health_ckeck.domain.repository.server_check_repository_interface import ServerCheckRepositoryInterface

logger = logging.getLogger(__name__)


async def delete_server_check_use_case(
    health_check_id: int,
    repository: ServerCheckRepositoryInterface
) -> None:
    existing = await repository.get_server_check(health_check_id)
    if not existing:
        raise ApplicationException(f"Server check {health_check_id} not found")

    await repository.delete_server_check(health_check_id)
