from pydantic import BaseModel
from datetime import datetime, timezone
from app.core.Exception import ApplicationException, SSHConnectionException
from app.modules.docker_registry.application.service.docker_metrics_service import DockerMetricService
from app.modules.server_registry.application.service.server_metrics_service import ServerMetricsService
from app.modules.server_registry.domain.entity.server import Server
from app.modules.server_registry.domain.entity.server_health import ServerHealth, HealthStatus
from app.modules.docker_registry.domain.entity.docker_container import DockerContainer
from app.modules.server_registry.domain.entity.server_history import HealthStatushistory, ServerHistory
from app.modules.server_registry.domain.repository.server_repository import ServerRepositoryInterface
from app.modules.docker_registry.domain.repository.docker_repository import DockerRepositoryInterface
import logging
logger = logging.getLogger(__name__)

class ServerMonitoringResult(BaseModel):
    server: Server
    current_health: ServerHealth
    containers: list[DockerContainer]

async def collect_all_servers_monitoring_use_case(
    server_repository: ServerRepositoryInterface,
    docker_repository: DockerRepositoryInterface,
    server_metrics_service: ServerMetricsService,
    docker_metrics_service: DockerMetricService
) -> list[ServerMonitoringResult]:
    
    servers = await server_repository.get_all_servers()
    
    if not servers:
        raise ApplicationException("No servers found")
    
    results = []
    
    for server in servers:
        if not server.id:
            continue
        
        server_history = None 
        
        try:
            metrics = await server_metrics_service.get_server_metrics(server)
            
            server_health = ServerHealth(
                server_id=server.id,
                status=HealthStatus.HEALTHY,
                cpu_usage=metrics.get('cpu_usage'),
                memory_usage=metrics.get('memory_usage'),
                disk_usage=metrics.get('disk_usage'),
                uptime=metrics.get('uptime'),
                checked_at=datetime.now(timezone.utc)
            )
            server_history = ServerHistory(
                server_id=server.id,
                status=HealthStatushistory.HEALTHY,
                cpu_usage=metrics.get('cpu_usage'),
                memory_usage=metrics.get('memory_usage'),
                disk_usage=metrics.get('disk_usage'),
                uptime=metrics.get('uptime'),
                checked_at=datetime.now(timezone.utc)
            )
        except SSHConnectionException:
            server_health = ServerHealth(
                server_id=server.id,
                status=HealthStatus.OFFLINE,
                checked_at=datetime.now(timezone.utc)
            )
            server_history = ServerHistory(  # Add this
                server_id=server.id,
                status=HealthStatushistory.OFFLINE,
                checked_at=datetime.now(timezone.utc)
            )
        except Exception as e:
            logger.error(f"Failed to collect metrics for {server.ip_address}: {e}", exc_info=True)
            server_health = ServerHealth(
                server_id=server.id,
                status=HealthStatus.ERROR,
                checked_at=datetime.now(timezone.utc)
            )
            server_history = ServerHistory(
                server_id=server.id,
                status=HealthStatushistory.ERROR,
                checked_at=datetime.now(timezone.utc)
            )
        
        existing_health = await server_repository.get_server_health(server.id)
        
        if existing_health:
            await server_repository.update_server_health(server.id, server_health)
        else:
            await server_repository.persist_server_health(server_health)
        
        await server_repository.persist_server_health_history(server_history)

        containers = []
        if server_health.status == HealthStatus.HEALTHY:
            try:
                docker_data = await docker_metrics_service.get_docker_metrics(server)
                
                for container_data in docker_data:
                    container = DockerContainer(**container_data)
                    
                    existing_container = await docker_repository.get_docker_container(
                        container.container_id,
                        server.id
                    )
                    
                    if existing_container:
                        persisted = await docker_repository.update_docker_container(container)
                    else:
                        persisted = await docker_repository.persist_docker_container(container)
                    
                    containers.append(persisted)
            except Exception as e:
                logger.error(f"Failed to collect containers for {server.ip_address}: {e}", exc_info=True)
                pass
        
        results.append(ServerMonitoringResult(
            server=server,
            current_health=server_health,
            containers=containers
        ))
    
    return results