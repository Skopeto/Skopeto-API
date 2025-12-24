from app.modules.server_registry.application.service.server_metrics_service import ServerMetricsService
from app.modules.server_registry.domain.entity.server_health import ServerHealth, HealthStatus
from app.modules.server_registry.domain.repository.server_repository import ServerRepositoryInterface
from datetime import datetime

async def register_server_health_use_case(
    server_id: int,
    server_repository: ServerRepositoryInterface,
    ssh_client: ServerMetricsService
) -> ServerHealth:
    server = server_repository.get_server(server_id)
    if not server:
        raise ValueError("Server not found")
    
    try:
        metrics = await ssh_client.get_server_metrics(server)
        
        server_health = ServerHealth(
            server_id=server_id,
            status=HealthStatus.HEALTHY,
            cpu_usage=metrics.get('cpu_usage'),
            memory_usage=metrics.get('memory_usage'),
            disk_usage=metrics.get('disk_usage'),
            uptime=metrics.get('uptime'),
            checked_at=datetime.utcnow()
        )
        
        server_repository.persist_server_health(server_health)
        return server_health
        
    except Exception as e:
        server_health = ServerHealth(
            server_id=server_id,
            status=HealthStatus.OFFLINE,
            checked_at=datetime.utcnow()
        )
        
        server_repository.persist_server_health(server_health)
        return server_health