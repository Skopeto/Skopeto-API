import logging
from app.modules.server_registry.application.service.server_metrics_service import ServerMetricsServiceInterface
from app.modules.server_registry.domain.entity.server_check_results import ServerCheckResults
from app.modules.server_registry.domain.repository.server_repository import ServerRepositoryInterface

logger = logging.getLogger(__name__)


async def get_server_health_use_case(
    server_id: int,
    server_repository: ServerRepositoryInterface,
    server_metrics_service: ServerMetricsServiceInterface
) -> list[ServerCheckResults]:
    """Get fresh server health metrics by collecting them from the server."""
    server = await server_repository.get_server(server_id)
    if not server:
        return []

    server_checks = await server_repository.get_server_checks()
    if not server_checks:
        return []

    return await server_metrics_service.get_server_metrics(server=server, server_checks=server_checks)
