from app.modules.database_registry.application.service.database_health_orchestration_service import (
    DatabaseHealthOrchestrationServiceInterface,
    ServerAndDatabaseHealthResponse
)


async def get_server_databases_with_health_use_case(
    server_id: int,
    orchestration_service: DatabaseHealthOrchestrationServiceInterface
) -> ServerAndDatabaseHealthResponse:
    """
    Collects database health for a specific server and its databases.
    Used for: Single server database health refresh
    """
    return await orchestration_service.collect_server_with_databases_health(server_id)
