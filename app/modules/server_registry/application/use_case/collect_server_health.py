from pydantic import BaseModel
from datetime import datetime
from app.modules.server_registry.application.service.server_metrics_service import ServerMetricsService
from app.modules.server_registry.domain.entity.server import Server
from app.modules.server_registry.domain.entity.server_health import ServerHealth, HealthStatus
from app.modules.server_registry.domain.repository.server_repository import ServerRepositoryInterface

class ServerWithHealth(BaseModel):
    server: Server
    health: ServerHealth

async def collect_server_health_use_case(
    server_id: int,
    server_repository: ServerRepositoryInterface,
    server_metrics_service: ServerMetricsService
) -> ServerWithHealth:
    
    server = server_repository.get_server(server_id)
    
    if not server:
        raise ValueError("Server not found")
    
    try:
        metrics = await server_metrics_service.get_server_metrics(server)
        
        server_health = ServerHealth(
            server_id=server_id,
            status=HealthStatus.HEALTHY,
            cpu_usage=metrics.get('cpu_usage'),
            memory_usage=metrics.get('memory_usage'),
            disk_usage=metrics.get('disk_usage'),
            uptime=metrics.get('uptime'),
            checked_at=datetime.now()
        )
    except Exception as e:
        server_health = ServerHealth(
            server_id=server_id,
            status=HealthStatus.OFFLINE,
            checked_at=datetime.now()
        )
    
    server_repository.persist_server_health(server_health)
    
    return ServerWithHealth(
        server=server,
        health=server_health
    )