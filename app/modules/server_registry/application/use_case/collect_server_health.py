from pydantic import BaseModel
from app.modules.server_registry.application.service.server_metrics_service import ServerMetricsService
from app.modules.server_registry.application.use_case.register_server_health import register_server_health_use_case
from app.modules.server_registry.domain.entity.server import Server
from app.modules.server_registry.domain.entity.server_health import ServerHealth
from app.modules.server_registry.domain.repository.server_repository import ServerRepositoryInterface

class ServerWithHealth(BaseModel):
    server: Server
    health: ServerHealth

async def collect_server_health_use_case(
    server_id: int,
    server_repository: ServerRepositoryInterface,
    ssh_client: ServerMetricsService
) -> ServerWithHealth:
    server = server_repository.get_server(server_id)
    if not server:
        raise ValueError("Server not found")
    
    health = await register_server_health_use_case(
        server_id,
        server_repository,
        ssh_client
    )
    
    return ServerWithHealth(
        server=server,
        health=health
    )