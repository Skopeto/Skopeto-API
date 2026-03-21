import pytest
from unittest.mock import AsyncMock
from datetime import datetime, timezone

from app.modules.server_registry.application.use_case.collect_server_metrics import collect_server_metrics_use_case
from app.modules.server_registry.domain.entity.server import Server
from app.modules.server_registry.domain.entity.server_check_results import ServerCheckResults, HealthStatus
from app.modules.server_health_ckeck.domain.entity.heallth_check import ServerCheck
from app.modules.server_health_ckeck.domain.enum.health_check_status import HealthCheckStatus
from app.core.Exception import ApplicationException, SSHConnectionException


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
        ),
        ServerCheck(
            health_check_id=2,
            name="memory_usage",
            command="free | grep Mem | awk '{print $3/$2 * 100.0}'",
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
            value=45.2,
            unit="%",
            uptime=45.2,
            checked_at=datetime.now(timezone.utc)
        ),
        ServerCheckResults(
            server_id=1,
            status=HealthStatus.HEALTHY,
            check_name="memory_usage",
            value=62.8,
            unit="%",
            uptime=62.8,
            checked_at=datetime.now(timezone.utc)
        )
    ]


@pytest.mark.asyncio
async def test_collect_server_metrics_success(
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

    results = await collect_server_metrics_use_case(
        server_id=server_id,
        server_repository=mock_server_repository,
        server_metrics_service=mock_server_metrics_service
    )

    assert len(results) == 2
    assert results[0].check_name == "cpu_usage"
    assert results[0].status == HealthStatus.HEALTHY
    assert results[1].check_name == "memory_usage"

    mock_server_repository.get_server.assert_called_once_with(server_id)
    mock_server_repository.get_server_checks.assert_called_once()
    mock_server_metrics_service.get_server_metrics.assert_called_once()
    # Should persist history for each check result
    assert mock_server_repository.persist_server_check_history.call_count == 2


@pytest.mark.asyncio
async def test_collect_server_metrics_ssh_connection_exception(
    mock_server_repository: AsyncMock,
    mock_server_metrics_service: AsyncMock,
    sample_server: Server,
    sample_server_checks: list[ServerCheck]
):
    server_id = 1
    mock_server_repository.get_server.return_value = sample_server
    mock_server_repository.get_server_checks.return_value = sample_server_checks
    mock_server_metrics_service.get_server_metrics.side_effect = SSHConnectionException("Connection failed")

    with pytest.raises(SSHConnectionException):
        await collect_server_metrics_use_case(
            server_id=server_id,
            server_repository=mock_server_repository,
            server_metrics_service=mock_server_metrics_service
        )


@pytest.mark.asyncio
async def test_collect_server_metrics_generic_exception(
    mock_server_repository: AsyncMock,
    mock_server_metrics_service: AsyncMock,
    sample_server: Server,
    sample_server_checks: list[ServerCheck]
):
    server_id = 1
    mock_server_repository.get_server.return_value = sample_server
    mock_server_repository.get_server_checks.return_value = sample_server_checks
    mock_server_metrics_service.get_server_metrics.side_effect = Exception("Unexpected error")

    with pytest.raises(Exception, match="Unexpected error"):
        await collect_server_metrics_use_case(
            server_id=server_id,
            server_repository=mock_server_repository,
            server_metrics_service=mock_server_metrics_service
        )


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
    mock_server_repository.persist_server_check_history.assert_not_called()
