import pytest
from unittest.mock import AsyncMock
from datetime import datetime

from app.modules.server_registry.application.use_case.collect_server_metrics import collect_server_metrics_use_case
from app.modules.server_registry.domain.entity.server import Server
from app.modules.server_registry.domain.entity.server_check_results import ServerHealth, HealthStatus
from app.core.Exception import ApplicationException, SSHConnectionException


@pytest.mark.asyncio
async def test_collect_server_metrics_success_healthy(
    mock_server_repository: AsyncMock,
    mock_server_metrics_service: AsyncMock,
    sample_server: Server
):
    server_id = 1
    mock_server_repository.get_server.return_value = sample_server
    mock_server_repository.get_server_health.return_value = None

    metrics_data = {
        'cpu_usage': 45.2,
        'memory_usage': 62.8,
        'disk_usage': 78.5,
        'uptime': '15 days, 3:24:10',
        'status': 'healthy'
    }
    mock_server_metrics_service.get_server_metrics.return_value = metrics_data

    result = await collect_server_metrics_use_case(
        server_id=server_id,
        server_repository=mock_server_repository,
        server_metrics_service=mock_server_metrics_service
    )

    assert result.server_id == server_id
    assert result.status == HealthStatus.HEALTHY
    assert result.cpu_usage == 45.2
    assert result.memory_usage == 62.8
    assert result.disk_usage == 78.5
    assert result.uptime == '15 days, 3:24:10'
    assert isinstance(result.checked_at, datetime)

    mock_server_repository.get_server.assert_called_once_with(server_id)
    mock_server_metrics_service.get_server_metrics.assert_called_once_with(sample_server)
    mock_server_repository.persist_server_health.assert_called_once()
    mock_server_repository.persist_server_health_history.assert_called_once()


@pytest.mark.asyncio
async def test_collect_server_metrics_timeout_status(
    mock_server_repository: AsyncMock,
    mock_server_metrics_service: AsyncMock,
    sample_server: Server
):
    server_id = 1
    mock_server_repository.get_server.return_value = sample_server
    mock_server_repository.get_server_health.return_value = None

    metrics_data = {
        'status': 'timeout',
        'cpu_usage': None,
        'memory_usage': None,
        'disk_usage': None,
        'uptime': None
    }
    mock_server_metrics_service.get_server_metrics.return_value = metrics_data

    result = await collect_server_metrics_use_case(
        server_id=server_id,
        server_repository=mock_server_repository,
        server_metrics_service=mock_server_metrics_service
    )

    assert result.server_id == server_id
    assert result.status == HealthStatus.OFFLINE
    assert result.cpu_usage is None
    assert result.memory_usage is None

    mock_server_repository.persist_server_health.assert_called_once()
    mock_server_repository.persist_server_health_history.assert_called_once()


@pytest.mark.asyncio
async def test_collect_server_metrics_error_status(
    mock_server_repository: AsyncMock,
    mock_server_metrics_service: AsyncMock,
    sample_server: Server
):
    server_id = 1
    mock_server_repository.get_server.return_value = sample_server
    mock_server_repository.get_server_health.return_value = None

    metrics_data = {
        'status': 'error',
        'cpu_usage': None,
        'memory_usage': None,
        'disk_usage': None,
        'uptime': None
    }
    mock_server_metrics_service.get_server_metrics.return_value = metrics_data

    result = await collect_server_metrics_use_case(
        server_id=server_id,
        server_repository=mock_server_repository,
        server_metrics_service=mock_server_metrics_service
    )

    assert result.server_id == server_id
    assert result.status == HealthStatus.ERROR


@pytest.mark.asyncio
async def test_collect_server_metrics_ssh_connection_exception(
    mock_server_repository: AsyncMock,
    mock_server_metrics_service: AsyncMock,
    sample_server: Server
):
    server_id = 1
    mock_server_repository.get_server.return_value = sample_server
    mock_server_repository.get_server_health.return_value = None
    mock_server_metrics_service.get_server_metrics.side_effect = SSHConnectionException("Connection failed")

    result = await collect_server_metrics_use_case(
        server_id=server_id,
        server_repository=mock_server_repository,
        server_metrics_service=mock_server_metrics_service
    )

    assert result.server_id == server_id
    assert result.status == HealthStatus.OFFLINE
    assert result.cpu_usage is None
    assert result.memory_usage is None
    assert result.disk_usage is None
    assert result.uptime is None

    mock_server_repository.persist_server_health.assert_called_once()
    mock_server_repository.persist_server_health_history.assert_called_once()


@pytest.mark.asyncio
async def test_collect_server_metrics_generic_exception(
    mock_server_repository: AsyncMock,
    mock_server_metrics_service: AsyncMock,
    sample_server: Server
):
    server_id = 1
    mock_server_repository.get_server.return_value = sample_server
    mock_server_repository.get_server_health.return_value = None
    mock_server_metrics_service.get_server_metrics.side_effect = Exception("Unexpected error")

    result = await collect_server_metrics_use_case(
        server_id=server_id,
        server_repository=mock_server_repository,
        server_metrics_service=mock_server_metrics_service
    )

    assert result.server_id == server_id
    assert result.status == HealthStatus.ERROR
    assert result.cpu_usage is None

    mock_server_repository.persist_server_health.assert_called_once()
    mock_server_repository.persist_server_health_history.assert_called_once()


@pytest.mark.asyncio
async def test_collect_server_metrics_updates_existing_health(
    mock_server_repository: AsyncMock,
    mock_server_metrics_service: AsyncMock,
    sample_server: Server,
    sample_server_health: ServerHealth
):
    server_id = 1
    mock_server_repository.get_server.return_value = sample_server
    mock_server_repository.get_server_health.return_value = sample_server_health

    metrics_data = {
        'cpu_usage': 50.0,
        'memory_usage': 70.0,
        'disk_usage': 80.0,
        'uptime': '20 days',
        'status': 'healthy'
    }
    mock_server_metrics_service.get_server_metrics.return_value = metrics_data

    result = await collect_server_metrics_use_case(
        server_id=server_id,
        server_repository=mock_server_repository,
        server_metrics_service=mock_server_metrics_service
    )

    assert result.status == HealthStatus.HEALTHY
    mock_server_repository.update_server_health.assert_called_once()
    mock_server_repository.persist_server_health.assert_not_called()
    mock_server_repository.persist_server_health_history.assert_called_once()


@pytest.mark.asyncio
async def test_collect_server_metrics_server_not_found(
    mock_server_repository: AsyncMock,
    mock_server_metrics_service: AsyncMock
):
    server_id = 999
    mock_server_repository.get_server.return_value = None

    with pytest.raises(ApplicationException, match="Server 999 not found"):
        await collect_server_metrics_use_case(
            server_id=server_id,
            server_repository=mock_server_repository,
            server_metrics_service=mock_server_metrics_service
        )

    mock_server_metrics_service.get_server_metrics.assert_not_called()
    mock_server_repository.persist_server_health.assert_not_called()
