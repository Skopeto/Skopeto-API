import logging
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

logger = logging.getLogger(__name__)

class ServerMonitoringResult(BaseModel):
    server: Server
    current_health: ServerHealth
    containers: list[DockerContainer]

async def collect_server_health_with_containers_use_case(
    server_id: int,
    server_repository: ServerRepositoryInterface,
    docker_repository: DockerRepositoryInterface,
    server_metrics_service: ServerMetricsService,
    docker_metrics_service: DockerMetricService
) -> ServerMonitoringResult:
    
    server = await server_repository.get_server(server_id)
    
    if not server:
        raise ApplicationException(f"Server {server_id} not found")
    
    try:
        metrics = await server_metrics_service.get_server_metrics(server)
        
        metrics_status = metrics.get('status', 'up')
        if metrics_status == 'timeout':
            health_status = HealthStatus.OFFLINE
            history_status = HealthStatushistory.OFFLINE
        elif metrics_status in ('down', 'error'):
            health_status = HealthStatus.ERROR
            history_status = HealthStatushistory.ERROR
        else:
            health_status = HealthStatus.HEALTHY
            history_status = HealthStatushistory.HEALTHY
        
        server_health = ServerHealth(
            server_id=server_id,
            status=health_status,
            cpu_usage=metrics.get('cpu_usage'),
            memory_usage=metrics.get('memory_usage'),
            disk_usage=metrics.get('disk_usage'),
            uptime=metrics.get('uptime'),
            checked_at=datetime.now(timezone.utc)
        )
        server_history = ServerHistory(
            server_id=server_id,
            status=history_status,
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
        server_history = ServerHistory(
            server_id=server_id,
            status=HealthStatushistory.OFFLINE,
            checked_at=datetime.now(timezone.utc)
        )
    except Exception as e:
        logger.error(f"Failed to collect metrics for {server.ip_address}: {e}", exc_info=True)
        server_health = ServerHealth(
            server_id=server_id,
            status=HealthStatus.ERROR,
            checked_at=datetime.now(timezone.utc)
        )
        server_history = ServerHistory(
            server_id=server_id,
            status=HealthStatushistory.ERROR,
            checked_at=datetime.now(timezone.utc)
        )
    
    existing = await server_repository.get_server_health(server_id)
    if existing:
        await server_repository.update_server_health(server_id, server_health)
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
                    container.name,
                    server_id
                )
                
                if existing_container and existing_container.status != container.status:
                    container.state_changed_at = datetime.now(timezone.utc)
                elif not existing_container:
                    container.state_changed_at = datetime.now(timezone.utc)
                
                if existing_container:
                    persisted = await docker_repository.update_docker_container(container)
                else:
                    persisted = await docker_repository.persist_docker_container(container)
                
                containers.append(persisted)
        except Exception as e:
            logger.error(f"Failed to collect containers for {server.ip_address}: {e}", exc_info=True)
    
    return ServerMonitoringResult(
        server=server,
        current_health=server_health,
        containers=containers
    )