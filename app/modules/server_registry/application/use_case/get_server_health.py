
from app.modules.server_registry.domain.entity.server_check_results import ServerCheckResults
from app.modules.server_registry.domain.repository.server_repository import (
    ServerRepositoryInterface,
)
import logging

logger = logging.getLogger(__name__)


async def get_server_health_use_case(
    server_id: int,
    server_repository: ServerRepositoryInterface,
) -> ServerCheckResults | None:
    server_health = await server_repository.get_server_health(server_id)
    return server_health
