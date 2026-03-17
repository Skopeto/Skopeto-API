import logging
from datetime import datetime, timezone
from app.core.Exception import ApplicationException, SSHConnectionException
from app.modules.server_registry.application.service.server_metrics_service import ServerMetricsServiceInterface
from app.modules.server_registry.domain.entity.server_check_results import ServerCheckResults, HealthStatus
from app.modules.server_registry.domain.entity.server_history import HealthStatushistory, ServerHistory
from app.modules.server_registry.domain.repository.server_repository import ServerRepositoryInterface

logger = logging.getLogger(__name__)

async def collect_server_metrics_use_case(
    server_id: int,
    server_repository: ServerRepositoryInterface,
    server_metrics_service: ServerMetricsServiceInterface
) -> ServerCheckResults:
    
    server = await server_repository.get_server(server_id)
    if not server:
        raise ApplicationException(f"Server {server_id} not found")
    
    try:
        server_checks = await server_repository.get_server_checks(server_id)
        metrics = await server_metrics_service.get_server_metrics(server=server, server_checks=server_checks)
        
        metrics_status = metrics.get('status', 'up')
        if metrics_status == 'timeout':
            health_status = HealthStatus.OFFLINE
            history_status = HealthStatushistory.OFFLINE
        elif metrics_status in ('down', 'error'):
            health_status = HealthStatus.ERROR
            history_status = HealthStatushistory.ERROR
        elif metrics_status == 'healthy':
            health_status = HealthStatus.HEALTHY
            history_status = HealthStatushistory.HEALTHY
        else:
            health_status = HealthStatus.UNHEALTHY
            history_status = HealthStatushistory.UNHEALTHY
        
        server_check_results = ServerCheckResults(
            server_id=server_id,
            status=health_status,
            check_name=metrics.get('check_name', 'unknown'),
            unit=metrics.get('unit'),
            uptime=metrics.get('uptime'),
            checked_at=datetime.now(timezone.utc)
        )
        server_history = ServerHistory(
            server_id=server_id,
            status=history_status,
            uptime=metrics.get('uptime'),
            checked_at=datetime.now(timezone.utc)
        )
    except SSHConnectionException:
        server_check_results = ServerCheckResults(
            server_id=server_id,
            status=HealthStatus.OFFLINE,
            check_name='unknown',
            unit=None,
            uptime=None,
            checked_at=datetime.now(timezone.utc)
        )
        server_history = ServerHistory(
            server_id=server_id,
            status=HealthStatushistory.OFFLINE,
            uptime=None,
            checked_at=datetime.now(timezone.utc)
        )
    except Exception as e:
        logger.error(f"Failed to collect metrics for {server.ip_address}: {e}", exc_info=True)
        server_check_results = ServerCheckResults(
            server_id=server_id,
            status=HealthStatus.ERROR,
            check_name='unknown',
            unit=None,
            uptime=None,
            checked_at=datetime.now(timezone.utc)
        )
        server_history = ServerHistory(
            server_id=server_id,
            status=HealthStatushistory.ERROR,
            uptime=None,
            checked_at=datetime.now(timezone.utc)
        )
    
    existing = await server_repository.get_server_check_results(server_id)
    if existing:
        await server_repository.update_server_check_results(server_id, server_check_results)
    else:
        await server_repository.persist_server_check_results(server_check_results)
    
    await server_repository.persist_server_health_history(server_history)
    
    return server_check_results