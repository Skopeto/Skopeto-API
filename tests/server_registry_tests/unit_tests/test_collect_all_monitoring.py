import pytest
from unittest.mock import AsyncMock, patch
from datetime import datetime, timezone

from app.core.Exception import ApplicationException, SSHConnectionException
from app.modules.server_registry.application.use_case.collect_all_monitoring import (
    collect_all_servers_monitoring_use_case,
    ServerMonitoringResult
)
from app.modules.server_registry.domain.entity.server import Server, ServerStatus
from app.modules.server_registry.domain.entity.server_health import HealthStatus
from app.modules.server_registry.domain.entity.server_history import HealthStatushistory
from app.modules.docker_registry.domain.entity.docker_container import DockerContainer
from app.modules.docker_registry.domain.entity.docker_status import ContainerStatus
from app.modules.server_registry.domain.repository.server_repository import ServerRepositoryInterface
from app.modules.docker_registry.domain.repository.docker_repository import DockerRepositoryInterface
from app.modules.server_registry.application.service.server_metrics_service import ServerMetricsService
from app.modules.docker_registry.application.service.docker_metrics_service import DockerMetricService


@pytest.mark.asyncio
@patch('app.modules.server_registry.application.use_case.collect_all_monitoring.datetime')
async def test_collect_all_monitoring_success_all_healthy(mock_datetime):
    """Test successful monitoring of all healthy servers with containers"""
    # Arrange
    fixed_time = datetime(2025, 12, 26, 12, 0, 0, tzinfo=timezone.utc)
    mock_datetime.now.return_value = fixed_time

    mock_server_repo = AsyncMock(spec=ServerRepositoryInterface)
    mock_docker_repo = AsyncMock(spec=DockerRepositoryInterface)
    mock_server_metrics_service = AsyncMock(spec=ServerMetricsService)
    mock_docker_metrics_service = AsyncMock(spec=DockerMetricService)

    server1 = Server(id=1, user_name="user1", ssh_password_encrypted="enc1",
                     ip_address="192.168.1.100", port=22, status=ServerStatus.UP)
    server2 = Server(id=2, user_name="user2", ssh_password_encrypted="enc2",
                     ip_address="192.168.1.101", port=22, status=ServerStatus.UP)

    metrics1 = {'cpu_usage': 25.5, 'memory_usage': 60.2, 'disk_usage': 45.0, 'uptime': 'up 5 days', 'server_id': 1}
    metrics2 = {'cpu_usage': 30.0, 'memory_usage': 55.0, 'disk_usage': 50.0, 'uptime': 'up 3 days', 'server_id': 2}

    container_data_1 = {'container_id': 'abc123', 'name': 'web-app', 'status': ContainerStatus.RUNNING,
                        'image': 'nginx:latest', 'ports': '80:80', 'server_id': 1}
    container_data_2 = {'container_id': 'def456', 'name': 'database', 'status': ContainerStatus.RUNNING,
                        'image': 'postgres:14', 'ports': '5432:5432', 'server_id': 2}

    mock_server_repo.get_all_servers.return_value = [server1, server2]

    async def get_server_metrics_side_effect(server):
        if server.id == 1:
            return metrics1
        return metrics2

    mock_server_metrics_service.get_server_metrics.side_effect = get_server_metrics_side_effect

    async def get_docker_metrics_side_effect(server):
        if server.id == 1:
            return [container_data_1]
        return [container_data_2]

    mock_docker_metrics_service.get_docker_metrics.side_effect = get_docker_metrics_side_effect

    mock_server_repo.get_server_health.return_value = None
    mock_docker_repo.get_docker_container.return_value = None

    container1 = DockerContainer(**container_data_1)
    container1.id = 1
    container2 = DockerContainer(**container_data_2)
    container2.id = 2

    async def persist_docker_container_side_effect(container):
        if container.container_id == 'abc123':
            return container1
        return container2

    mock_docker_repo.persist_docker_container.side_effect = persist_docker_container_side_effect

    # Act
    results = await collect_all_servers_monitoring_use_case(
        server_repository=mock_server_repo,
        docker_repository=mock_docker_repo,
        server_metrics_service=mock_server_metrics_service,
        docker_metrics_service=mock_docker_metrics_service
    )

    # Assert
    assert len(results) == 2
    assert all(isinstance(r, ServerMonitoringResult) for r in results)

    assert results[0].server.id == 1
    assert results[0].current_health.status == HealthStatus.HEALTHY
    assert len(results[0].containers) == 1
    assert results[0].containers[0].container_id == 'abc123'

    assert results[1].server.id == 2
    assert results[1].current_health.status == HealthStatus.HEALTHY
    assert len(results[1].containers) == 1
    assert results[1].containers[0].container_id == 'def456'

    assert mock_server_repo.persist_server_health.call_count == 2
    assert mock_server_repo.persist_server_health_history.call_count == 2


@pytest.mark.asyncio
@patch('app.modules.server_registry.application.use_case.collect_all_monitoring.datetime')
async def test_collect_all_monitoring_mixed_health_status(mock_datetime):
    """Test monitoring with mixed health statuses"""
    # Arrange
    fixed_time = datetime(2025, 12, 26, 12, 0, 0, tzinfo=timezone.utc)
    mock_datetime.now.return_value = fixed_time

    mock_server_repo = AsyncMock(spec=ServerRepositoryInterface)
    mock_docker_repo = AsyncMock(spec=DockerRepositoryInterface)
    mock_server_metrics_service = AsyncMock(spec=ServerMetricsService)
    mock_docker_metrics_service = AsyncMock(spec=DockerMetricService)

    server1 = Server(id=1, user_name="user1", ssh_password_encrypted="enc1",
                     ip_address="192.168.1.100", port=22, status=ServerStatus.UP)
    server2 = Server(id=2, user_name="user2", ssh_password_encrypted="enc2",
                     ip_address="192.168.1.101", port=22, status=ServerStatus.UP)

    mock_server_repo.get_all_servers.return_value = [server1, server2]

    metrics1 = {'cpu_usage': 25.5, 'memory_usage': 60.2, 'disk_usage': 45.0, 'uptime': 'up 5 days', 'server_id': 1}

    async def get_server_metrics_side_effect(server):
        if server.id == 1:
            return metrics1
        raise SSHConnectionException("Connection timeout")

    mock_server_metrics_service.get_server_metrics.side_effect = get_server_metrics_side_effect

    container_data = {'container_id': 'abc123', 'name': 'web-app', 'status': ContainerStatus.RUNNING,
                      'image': 'nginx:latest', 'ports': '80:80', 'server_id': 1}

    mock_docker_metrics_service.get_docker_metrics.return_value = [container_data]
    mock_server_repo.get_server_health.return_value = None
    mock_docker_repo.get_docker_container.return_value = None

    container = DockerContainer(**container_data)
    container.id = 1
    mock_docker_repo.persist_docker_container.return_value = container

    # Act
    results = await collect_all_servers_monitoring_use_case(
        server_repository=mock_server_repo,
        docker_repository=mock_docker_repo,
        server_metrics_service=mock_server_metrics_service,
        docker_metrics_service=mock_docker_metrics_service
    )

    # Assert
    assert len(results) == 2

    # Server 1: HEALTHY with containers
    assert results[0].current_health.status == HealthStatus.HEALTHY
    assert len(results[0].containers) == 1

    # Server 2: OFFLINE with no containers
    assert results[1].current_health.status == HealthStatus.OFFLINE
    assert len(results[1].containers) == 0


@pytest.mark.asyncio
@patch('app.modules.server_registry.application.use_case.collect_all_monitoring.datetime')
async def test_collect_all_monitoring_server_with_error_status(mock_datetime, caplog):
    """Test monitoring when server metrics collection raises generic exception"""
    # Arrange
    fixed_time = datetime(2025, 12, 26, 12, 0, 0, tzinfo=timezone.utc)
    mock_datetime.now.return_value = fixed_time

    mock_server_repo = AsyncMock(spec=ServerRepositoryInterface)
    mock_docker_repo = AsyncMock(spec=DockerRepositoryInterface)
    mock_server_metrics_service = AsyncMock(spec=ServerMetricsService)
    mock_docker_metrics_service = AsyncMock(spec=DockerMetricService)

    server = Server(id=1, user_name="user1", ssh_password_encrypted="enc1",
                    ip_address="192.168.1.100", port=22, status=ServerStatus.UP)

    mock_server_repo.get_all_servers.return_value = [server]
    mock_server_metrics_service.get_server_metrics.side_effect = Exception("Unexpected error")
    mock_server_repo.get_server_health.return_value = None

    # Act
    results = await collect_all_servers_monitoring_use_case(
        server_repository=mock_server_repo,
        docker_repository=mock_docker_repo,
        server_metrics_service=mock_server_metrics_service,
        docker_metrics_service=mock_docker_metrics_service
    )

    # Assert
    assert len(results) == 1
    assert results[0].current_health.status == HealthStatus.ERROR
    assert len(results[0].containers) == 0
    assert "Failed to collect metrics" in caplog.text


@pytest.mark.asyncio
@patch('app.modules.server_registry.application.use_case.collect_all_monitoring.datetime')
async def test_collect_all_monitoring_container_collection_failure(mock_datetime, caplog):
    """Test monitoring when container collection fails for healthy server"""
    # Arrange
    fixed_time = datetime(2025, 12, 26, 12, 0, 0, tzinfo=timezone.utc)
    mock_datetime.now.return_value = fixed_time

    mock_server_repo = AsyncMock(spec=ServerRepositoryInterface)
    mock_docker_repo = AsyncMock(spec=DockerRepositoryInterface)
    mock_server_metrics_service = AsyncMock(spec=ServerMetricsService)
    mock_docker_metrics_service = AsyncMock(spec=DockerMetricService)

    server = Server(id=1, user_name="user1", ssh_password_encrypted="enc1",
                    ip_address="192.168.1.100", port=22, status=ServerStatus.UP)

    mock_server_repo.get_all_servers.return_value = [server]
    mock_server_metrics_service.get_server_metrics.return_value = {
        'cpu_usage': 25.5, 'memory_usage': 60.2, 'disk_usage': 45.0, 'uptime': 'up 5 days', 'server_id': 1
    }
    mock_server_repo.get_server_health.return_value = None
    mock_docker_metrics_service.get_docker_metrics.side_effect = Exception("Docker connection failed")

    # Act
    results = await collect_all_servers_monitoring_use_case(
        server_repository=mock_server_repo,
        docker_repository=mock_docker_repo,
        server_metrics_service=mock_server_metrics_service,
        docker_metrics_service=mock_docker_metrics_service
    )

    # Assert
    assert len(results) == 1
    assert results[0].current_health.status == HealthStatus.HEALTHY
    assert len(results[0].containers) == 0  # Containers collection failed
    assert "Failed to collect containers" in caplog.text


@pytest.mark.asyncio
async def test_collect_all_monitoring_no_servers():
    """Test when no servers exist in database"""
    # Arrange
    mock_server_repo = AsyncMock(spec=ServerRepositoryInterface)
    mock_docker_repo = AsyncMock(spec=DockerRepositoryInterface)
    mock_server_metrics_service = AsyncMock(spec=ServerMetricsService)
    mock_docker_metrics_service = AsyncMock(spec=DockerMetricService)

    mock_server_repo.get_all_servers.return_value = []

    # Act & Assert
    with pytest.raises(ApplicationException, match="No servers found"):
        await collect_all_servers_monitoring_use_case(
            server_repository=mock_server_repo,
            docker_repository=mock_docker_repo,
            server_metrics_service=mock_server_metrics_service,
            docker_metrics_service=mock_docker_metrics_service
        )


@pytest.mark.asyncio
@patch('app.modules.server_registry.application.use_case.collect_all_monitoring.datetime')
async def test_collect_all_monitoring_server_without_id(mock_datetime):
    """Test that servers without ID are skipped"""
    # Arrange
    fixed_time = datetime(2025, 12, 26, 12, 0, 0, tzinfo=timezone.utc)
    mock_datetime.now.return_value = fixed_time

    mock_server_repo = AsyncMock(spec=ServerRepositoryInterface)
    mock_docker_repo = AsyncMock(spec=DockerRepositoryInterface)
    mock_server_metrics_service = AsyncMock(spec=ServerMetricsService)
    mock_docker_metrics_service = AsyncMock(spec=DockerMetricService)

    server_with_id = Server(id=1, user_name="user1", ssh_password_encrypted="enc1",
                            ip_address="192.168.1.100", port=22, status=ServerStatus.UP)
    server_without_id = Server(id=None, user_name="user2", ssh_password_encrypted="enc2",
                               ip_address="192.168.1.101", port=22, status=ServerStatus.UP)

    mock_server_repo.get_all_servers.return_value = [server_without_id, server_with_id]
    mock_server_metrics_service.get_server_metrics.return_value = {
        'cpu_usage': 25.5, 'memory_usage': 60.2, 'disk_usage': 45.0, 'uptime': 'up 5 days', 'server_id': 1
    }
    mock_server_repo.get_server_health.return_value = None
    mock_docker_metrics_service.get_docker_metrics.return_value = []

    # Act
    results = await collect_all_servers_monitoring_use_case(
        server_repository=mock_server_repo,
        docker_repository=mock_docker_repo,
        server_metrics_service=mock_server_metrics_service,
        docker_metrics_service=mock_docker_metrics_service
    )

    # Assert
    assert len(results) == 1  # Only server with ID is processed
    assert results[0].server.id == 1
    # Server metrics service should only be called once (for server with ID)
    mock_server_metrics_service.get_server_metrics.assert_called_once()
