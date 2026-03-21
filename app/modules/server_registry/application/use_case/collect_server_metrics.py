import logging
from app.core.Exception import ApplicationException, SSHConnectionException
from app.modules.server_registry.application.service.server_metrics_service import ServerMetricsServiceInterface
from app.modules.server_registry.domain.entity.server_check_results import ServerCheckResults
from app.modules.server_registry.domain.entity.server_check_history import ServerCheckHistory
from app.modules.server_registry.domain.repository.server_repository import ServerRepositoryInterface

logger = logging.getLogger(__name__)


async def collect_server_metrics_use_case(
    server_id: int,
    server_repository: ServerRepositoryInterface,
    server_metrics_service: ServerMetricsServiceInterface
) -> list[ServerCheckResults]:

    server = await server_repository.get_server(server_id)
    if not server:
        raise ApplicationException(f"Server {server_id} not found")

    try:
        server_checks = await server_repository.get_server_checks()
        results = await server_metrics_service.get_server_metrics(server=server, server_checks=server_checks)

        # Persist each check result to history
        for result in results:
            server_check_history = ServerCheckHistory(
                server_id=result.server_id,
                status=result.status,
                check_name=result.check_name,
                value=result.value,
                unit=result.unit,
                uptime=result.uptime,
                checked_at=result.checked_at
            )
            await server_repository.persist_server_check_history(server_check_history)

        return results

    except SSHConnectionException:
        logger.error(f"SSH connection failed for server {server_id}")
        raise
    except Exception as e:
        logger.error(f"Failed to collect metrics for {server.ip_address}: {e}", exc_info=True)
        raise
