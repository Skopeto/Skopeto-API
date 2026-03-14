from app.modules.database_registry.application.service.database_health_orchestration_service import (
    DatabaseHealthOrchestrationServiceInterface,
    ServerAndDatabaseHealthResponse
)


async def get_all_databases_with_health_use_case(
    orchestration_service: DatabaseHealthOrchestrationServiceInterface
) -> list[ServerAndDatabaseHealthResponse]:
    """
    Collects database health for all servers and their databases.
    Used for: Database tab refresh
    """
    return await orchestration_service.collect_all_servers_with_databases_health()
