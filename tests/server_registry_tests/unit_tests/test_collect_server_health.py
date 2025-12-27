import pytest
from unittest.mock import AsyncMock, patch
from datetime import datetime, timezone

from app.core.Exception import ApplicationException, SSHConnectionException
from app.modules.server_registry.application.use_case.collect_server_health_with_containers import (
    collect_server_health_with_containers_use_case,
    ServerMonitoringResult
)
from app.modules.server_registry.domain.entity.server import Server, ServerStatus
from app.modules.server_registry.domain.entity.server_health import ServerHealth, HealthStatus
from app.modules.server_registry.domain.entity.server_history import HealthStatushistory


@pytest.mark.asyncio
@patch('app.modules.server_registry.application.use_case.collect_server_health_with_containers.datetime')
async def test_collect_server_health_success_healthy_new(
    mock_datetime,
    mock_server_repository: AsyncMock,
    mock_docker_repository: AsyncMock,
    mock_server_metrics_service: AsyncMock,
    mock_docker_metrics_service: AsyncMock,
    sample_server: Server,
    sample_server_metrics: dict
):
    """Test successful health collection with HEALTHY status for new server"""
    # Arrange
    fixed_time = datetime(2025, 12, 26, 12, 0, 0, tzinfo=timezone.utc)
    mock_datetime.now.return_value = fixed_time

    mock_server_repository.get_server.return_value = sample_server
    mock_server_metrics_service.get_server_metrics.return_value = sample_server_metrics
    mock_server_repository.get_server_health.return_value = None  # No existing health
    mock_docker_metrics_service.get_docker_metrics.return_value = []

    # Act
    result = await collect_server_health_with_containers_use_case(
        server_id=1,
        server_repository=mock_server_repository,
        docker_repository=mock_docker_repository,
        server_metrics_service=mock_server_metrics_service,
        docker_metrics_service=mock_docker_metrics_service
    )

    # Assert
    assert isinstance(result, ServerMonitoringResult)
    assert result.server.id == 1
    assert result.current_health.status == HealthStatus.HEALTHY
    assert result.current_health.cpu_usage == 25.5
    assert result.current_health.memory_usage == 60.2
    assert result.current_health.disk_usage == 45.0
    assert result.current_health.uptime == 'up 5 days'
    assert result.current_health.checked_at == fixed_time
    assert result.containers == []

    mock_server_repository.get_server.assert_called_once_with(1)
    mock_server_metrics_service.get_server_metrics.assert_called_once_with(sample_server)
    mock_server_repository.persist_server_health.assert_called_once()
    mock_server_repository.update_server_health.assert_not_called()
    mock_server_repository.persist_server_health_history.assert_called_once()


@pytest.mark.asyncio
@patch('app.modules.server_registry.application.use_case.collect_server_health_with_containers.datetime')
async def test_collect_server_health_success_healthy_update_existing(
    mock_datetime,
    mock_server_repository: AsyncMock,
    mock_docker_repository: AsyncMock,
    mock_server_metrics_service: AsyncMock,
    mock_docker_metrics_service: AsyncMock,
    sample_server: Server,
    sample_server_health: ServerHealth,
    sample_server_metrics: dict
):
    """Test successful health collection updating existing health record"""
    # Arrange
    fixed_time = datetime(2025, 12, 26, 12, 0, 0, tzinfo=timezone.utc)
    mock_datetime.now.return_value = fixed_time

    mock_server_repository.get_server.return_value = sample_server
    mock_server_metrics_service.get_server_metrics.return_value = sample_server_metrics
    mock_server_repository.get_server_health.return_value = sample_server_health
    mock_docker_metrics_service.get_docker_metrics.return_value = []

    # Act
    result = await collect_server_health_with_containers_use_case(
        server_id=1,
        server_repository=mock_server_repository,
        docker_repository=mock_docker_repository,
        server_metrics_service=mock_server_metrics_service,
        docker_metrics_service=mock_docker_metrics_service
    )

    # Assert
    assert isinstance(result, ServerMonitoringResult)
    assert result.current_health.status == HealthStatus.HEALTHY
    assert result.containers == []
    mock_server_repository.update_server_health.assert_called_once()
    mock_server_repository.persist_server_health.assert_not_called()
    mock_server_repository.persist_server_health_history.assert_called_once()


@pytest.mark.asyncio
@patch('app.modules.server_registry.application.use_case.collect_server_health_with_containers.datetime')
async def test_collect_server_health_ssh_connection_failure(
    mock_datetime,
    mock_server_repository: AsyncMock,
    mock_docker_repository: AsyncMock,
    mock_server_metrics_service: AsyncMock,
    mock_docker_metrics_service: AsyncMock,
    sample_server: Server
):
    """Test health collection when SSH connection fails"""
    # Arrange
    fixed_time = datetime(2025, 12, 26, 12, 0, 0, tzinfo=timezone.utc)
    mock_datetime.now.return_value = fixed_time

    mock_server_repository.get_server.return_value = sample_server
    mock_server_metrics_service.get_server_metrics.side_effect = SSHConnectionException("Connection timeout")
    mock_server_repository.get_server_health.return_value = None

    # Act
    result = await collect_server_health_with_containers_use_case(
        server_id=1,
        server_repository=mock_server_repository,
        docker_repository=mock_docker_repository,
        server_metrics_service=mock_server_metrics_service,
        docker_metrics_service=mock_docker_metrics_service
    )

    # Assert
    assert isinstance(result, ServerMonitoringResult)
    assert result.server.id == 1
    assert result.current_health.status == HealthStatus.OFFLINE
    assert result.current_health.cpu_usage is None
    assert result.current_health.memory_usage is None
    assert result.current_health.disk_usage is None
    assert result.current_health.uptime is None
    assert result.current_health.checked_at == fixed_time
    assert result.containers == []

    mock_server_repository.persist_server_health.assert_called_once()

    # Verify history was created with OFFLINE status
    history_call = mock_server_repository.persist_server_health_history.call_args[0][0]
    assert history_call.status == HealthStatushistory.OFFLINE


@pytest.mark.asyncio
@patch('app.modules.server_registry.application.use_case.collect_server_health_with_containers.datetime')
async def test_collect_server_health_general_exception(
    mock_datetime,
    mock_server_repository: AsyncMock,
    mock_docker_repository: AsyncMock,
    mock_server_metrics_service: AsyncMock,
    mock_docker_metrics_service: AsyncMock,
    sample_server: Server,
    caplog
):
    """Test health collection when a general exception occurs"""
    # Arrange
    fixed_time = datetime(2025, 12, 26, 12, 0, 0, tzinfo=timezone.utc)
    mock_datetime.now.return_value = fixed_time

    mock_server_repository.get_server.return_value = sample_server
    mock_server_metrics_service.get_server_metrics.side_effect = Exception("Unexpected error")
    mock_server_repository.get_server_health.return_value = None

    # Act
    result = await collect_server_health_with_containers_use_case(
        server_id=1,
        server_repository=mock_server_repository,
        docker_repository=mock_docker_repository,
        server_metrics_service=mock_server_metrics_service,
        docker_metrics_service=mock_docker_metrics_service
    )

    # Assert
    assert isinstance(result, ServerMonitoringResult)
    assert result.current_health.status == HealthStatus.ERROR
    assert result.current_health.cpu_usage is None
    assert result.current_health.memory_usage is None
    assert result.current_health.disk_usage is None
    assert result.current_health.uptime is None
    assert result.containers == []

    # Verify error was logged
    assert "Failed to collect metrics" in caplog.text

    mock_server_repository.persist_server_health.assert_called_once()

    # Verify history was created with ERROR status
    history_call = mock_server_repository.persist_server_health_history.call_args[0][0]
    assert history_call.status == HealthStatushistory.ERROR


@pytest.mark.asyncio
async def test_collect_server_health_server_not_found(
    mock_server_repository: AsyncMock,
    mock_docker_repository: AsyncMock,
    mock_server_metrics_service: AsyncMock,
    mock_docker_metrics_service: AsyncMock
):
    """Test when server is not found"""
    # Arrange
    mock_server_repository.get_server.return_value = None

    # Act & Assert
    with pytest.raises(ApplicationException, match="Server 1 not found"):
        await collect_server_health_with_containers_use_case(
            server_id=1,
            server_repository=mock_server_repository,
            docker_repository=mock_docker_repository,
            server_metrics_service=mock_server_metrics_service,
            docker_metrics_service=mock_docker_metrics_service
        )

    mock_server_repository.get_server.assert_called_once_with(1)
    mock_server_metrics_service.get_server_metrics.assert_not_called()
