from pydantic import BaseModel
from datetime import datetime, timezone
from app.core.Exception import ApplicationException, SSHConnectionException
from app.modules.server_registry.application.service.server_metrics_service import ServerMetricsService
from app.modules.server_registry.domain.entity.server import Server
from app.modules.server_registry.domain.entity.server_health import ServerHealth, HealthStatus
from app.modules.server_registry.domain.entity.server_history import HealthStatushistory, ServerHistory
from app.modules.server_registry.domain.repository.server_repository import ServerRepositoryInterface

class ServerWithHealth(BaseModel):
    server: Server
    health: ServerHealth

async def collect_server_health_use_case(
    server_id: int,
    server_repository: ServerRepositoryInterface,
    server_metrics_service: ServerMetricsService
) -> ServerWithHealth:
    
    server = await server_repository.get_server(server_id)
    
    if not server:
        raise ApplicationException(f"Server {server_id} not found")
    
    try:
        metrics = await server_metrics_service.get_server_metrics(server)
        
        server_health = ServerHealth(
            server_id=server_id,
            status=HealthStatus.HEALTHY,
            cpu_usage=metrics.get('cpu_usage'),
            memory_usage=metrics.get('memory_usage'),
            disk_usage=metrics.get('disk_usage'),
            uptime=metrics.get('uptime'),
            checked_at=datetime.now(timezone.utc)
        )
        server_history = ServerHistory(
            server_id=server_id,
            status=HealthStatushistory.HEALTHY,
            cpu_usage=metrics.get('cpu_usage'),
            memory_usage=metrics.get('memory_usage'),
            disk_usage=metrics.get('disk_usage'),
            uptime=metrics.get('uptime'),
            checked_at=datetime.now(timezone.utc)
        )
    except SSHConnectionException:
        server_health = ServerHealth(
            server_id=server_id,
            status=HealthStatus.OFFLINE,
            checked_at=datetime.now(timezone.utc)
        )
    except Exception:
        server_health = ServerHealth(
            server_id=server_id,
            status=HealthStatus.ERROR,
            checked_at=datetime.now(timezone.utc)
        )
    
    existing = await server_repository.get_server_health(server_id)
    
    if existing:
        await server_repository.update_server_health(server_id, server_health)
    else:
        await server_repository.persist_server_health(server_health)
    
    await server_repository.persist_server_health_history(server_history)
    
    return ServerWithHealth(
        server=server,
        health=server_health
    )