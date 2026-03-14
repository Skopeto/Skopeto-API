import logging
from app.modules.server_health_ckeck.domain.entity.heallth_check import ServerCheck
from app.modules.server_health_ckeck.domain.repository.server_check_repository_interface import ServerCheckRepositoryInterface

logger = logging.getLogger(__name__)

async def get_server_check(
    repository: ServerCheckRepositoryInterface
) -> list[ServerCheck]:
    """
    Fetch all server checks from the repository and map them to ServerCheck objects.

    Returns an empty list if no server checks exist.
    """
    try:
        rows = await repository.get_server_checks()
        if not rows:
            return []

        server_checks = [
            ServerCheck(
                health_check_id=row["health_check_id"],
                name=row["name"],
                command=row["command"],
                threshold=row["threshold"],
                operator=row["operator"],
                check_status=row["check_status"]
            )
            for row in rows
        ]
        return server_checks
    except Exception as e:
        logger.error(f"Failed to fetch server checks: {str(e)}")
        raise