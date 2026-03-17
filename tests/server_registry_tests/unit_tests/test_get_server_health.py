import pytest
from unittest.mock import AsyncMock
from datetime import datetime, timezone

from app.modules.server_registry.application.use_case.get_server_health import get_server_health_use_case
from app.modules.server_registry.domain.entity.server_check_results import ServerHealth, HealthStatus


@pytest.mark.asyncio
async def test_get_server_health_success(
    mock_server_repository: AsyncMock,
    sample_server_health: ServerHealth
):
    server_id = 1
    mock_server_repository.get_server_health.return_value = sample_server_health

    result = await get_server_health_use_case(
        server_id=server_id,
        server_repository=mock_server_repository
    )

    assert result is not None
    assert result.server_id == server_id
    assert result.status == HealthStatus.HEALTHY
    assert result.cpu_usage == 25.5
    assert result.memory_usage == 60.2
    assert result.disk_usage == 45.0
    assert result.uptime == "up 5 days"
    mock_server_repository.get_server_health.assert_called_once_with(server_id)


@pytest.mark.asyncio
async def test_get_server_health_not_found(
    mock_server_repository: AsyncMock
):
    server_id = 999
    mock_server_repository.get_server_health.return_value = None

    result = await get_server_health_use_case(
        server_id=server_id,
        server_repository=mock_server_repository
    )

    assert result is None
    mock_server_repository.get_server_health.assert_called_once_with(server_id)


@pytest.mark.asyncio
async def test_get_server_health_offline_status(
    mock_server_repository: AsyncMock
):
    server_id = 1
    offline_health = ServerHealth(
        server_id=server_id,
        status=HealthStatus.OFFLINE,
        cpu_usage=None,
        memory_usage=None,
        disk_usage=None,
        uptime=None,
        checked_at=datetime.now(timezone.utc)
    )
    mock_server_repository.get_server_health.return_value = offline_health

    result = await get_server_health_use_case(
        server_id=server_id,
        server_repository=mock_server_repository
    )

    assert result is not None
    assert result.status == HealthStatus.OFFLINE
    assert result.cpu_usage is None
    assert result.memory_usage is None
    assert result.disk_usage is None
    assert result.uptime is None


@pytest.mark.asyncio
async def test_get_server_health_error_status(
    mock_server_repository: AsyncMock
):
    server_id = 1
    error_health = ServerHealth(
        server_id=server_id,
        status=HealthStatus.ERROR,
        checked_at=datetime.now(timezone.utc)
    )
    mock_server_repository.get_server_health.return_value = error_health

    result = await get_server_health_use_case(
        server_id=server_id,
        server_repository=mock_server_repository
    )

    assert result is not None
    assert result.status == HealthStatus.ERROR
    mock_server_repository.get_server_health.assert_called_once_with(server_id)
