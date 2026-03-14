import logging
from app.modules.server_health_ckeck.domain.entity.heallth_check import ServerCheck
from app.modules.server_health_ckeck.domain.repository.server_check_repository_interface import ServerCheckRepositoryInterface

logger = logging.getLogger(__name__)

async def get_server_check(
    repository: ServerCheckRepositoryInterface
) -> list[ServerCheck]:
    try:
        server_checks = await repository.get_server_checks()
        if not server_checks:
            return []
        return server_checks 
    except Exception as e:
        logger.error(f"Failed to fetch server checks: {str(e)}")
        raise