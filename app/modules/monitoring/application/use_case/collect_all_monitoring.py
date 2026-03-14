import asyncio
from app.core.Exception import ApplicationException
from app.modules.monitoring.application.service.monitoring_orchestration_service import MonitoringOrchestrationServiceInterface
from app.modules.server_registry.domain.repository.server_repository import ServerRepositoryInterface


async def collect_all_monitoring_use_case(
    server_repository: ServerRepositoryInterface,
    monitoring_service: MonitoringOrchestrationServiceInterface
) -> list[dict]:
    """
    Collects complete monitoring data for all servers.
    Includes: server health, containers, and databases.
    Used for: Dashboard full refresh
    """
    servers = await server_repository.get_all_servers()

    if not servers:
        raise ApplicationException("No servers found")

    results = await asyncio.gather(
        *[monitoring_service.collect_single_server_monitoring(server) for server in servers],
        return_exceptions=False
    )

    return results
