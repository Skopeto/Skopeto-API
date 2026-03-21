import pytest
from unittest.mock import AsyncMock
from datetime import datetime, timezone

from app.modules.server_registry.application.use_case.get_server_health import get_server_health_use_case
from app.modules.server_registry.domain.entity.server import Server
from app.modules.server_registry.domain.entity.server_check_results import ServerCheckResults, HealthStatus
from app.modules.server_health_ckeck.domain.entity.heallth_check import ServerCheck
from app.modules.server_health_ckeck.domain.enum.health_check_status import HealthCheckStatus


@pytest.fixture
def sample_server_checks() -> list[ServerCheck]:
    return [
        ServerCheck(
            health_check_id=1,
            name="cpu_usage",
            command="top -bn1 | grep 'Cpu(s)' | awk '{print $2}'",
            threshold=80,
            operator="<",
            unit="%",
            check_status=HealthCheckStatus.ACTIVE
        )
    ]


@pytest.fixture
def sample_check_results() -> list[ServerCheckResults]:
    return [
        ServerCheckResults(
            server_id=1,
            status=HealthStatus.HEALTHY,
            check_name="cpu_usage",
            value=25.5,
            unit="%",
            uptime=25.5,
            checked_at=datetime.now(timezone.utc)
        )
    ]


@pytest.mark.asyncio
async def test_get_server_health_success(
    mock_server_repository: AsyncMock,
    mock_server_metrics_service: AsyncMock,
    sample_server: Server,
    sample_server_checks: list[ServerCheck],
    sample_check_results: list[ServerCheckResults]
):
    server_id = 1
    mock_server_repository.get_server.return_value = sample_server
    mock_server_repository.get_server_checks.return_value = sample_server_checks
    mock_server_metrics_service.get_server_metrics.return_value = sample_check_results

    results = await get_server_health_use_case(
        server_id=server_id,
        server_repository=mock_server_repository,
        server_metrics_service=mock_server_metrics_service
    )

    assert len(results) == 1
    assert results[0].server_id == server_id
    assert results[0].status == HealthStatus.HEALTHY
    assert results[0].check_name == "cpu_usage"
    assert results[0].value == 25.5
    mock_server_repository.get_server.assert_called_once_with(server_id)
    mock_server_repository.get_server_checks.assert_called_once()


@pytest.mark.asyncio
async def test_get_server_health_server_not_found(
    mock_server_repository: AsyncMock,
    mock_server_metrics_service: AsyncMock
):
    server_id = 999
    mock_server_repository.get_server.return_value = None

    results = await get_server_health_use_case(
        server_id=server_id,
        server_repository=mock_server_repository,
        server_metrics_service=mock_server_metrics_service
    )

    assert results == []
    mock_server_metrics_service.get_server_metrics.assert_not_called()


@pytest.mark.asyncio
async def test_get_server_health_no_checks_configured(
    mock_server_repository: AsyncMock,
    mock_server_metrics_service: AsyncMock,
    sample_server: Server
):
    server_id = 1
    mock_server_repository.get_server.return_value = sample_server
    mock_server_repository.get_server_checks.return_value = []

    results = await get_server_health_use_case(
        server_id=server_id,
        server_repository=mock_server_repository,
        server_metrics_service=mock_server_metrics_service
    )

    assert results == []
    mock_server_metrics_service.get_server_metrics.assert_not_called()


@pytest.mark.asyncio
async def test_get_server_health_offline_status(
    mock_server_repository: AsyncMock,
    mock_server_metrics_service: AsyncMock,
    sample_server: Server,
    sample_server_checks: list[ServerCheck]
):
    server_id = 1
    offline_results = [
        ServerCheckResults(
            server_id=server_id,
            status=HealthStatus.OFFLINE,
            check_name="cpu_usage",
            value=0.0,
            unit="%",
            uptime=None,
            checked_at=datetime.now(timezone.utc)
        )
    ]
    mock_server_repository.get_server.return_value = sample_server
    mock_server_repository.get_server_checks.return_value = sample_server_checks
    mock_server_metrics_service.get_server_metrics.return_value = offline_results

    results = await get_server_health_use_case(
        server_id=server_id,
        server_repository=mock_server_repository,
        server_metrics_service=mock_server_metrics_service
    )

    assert len(results) == 1
    assert results[0].status == HealthStatus.OFFLINE
