import pytest
from unittest.mock import AsyncMock
from datetime import datetime, timezone

from app.modules.server_registry.domain.repository.server_repository import ServerRepositoryInterface
from app.modules.docker_registry.domain.repository.docker_repository import DockerRepositoryInterface
from app.modules.server_registry.domain.entity.server import Server, ServerStatus
from app.modules.server_registry.domain.entity.server_check_results import ServerCheckResults, HealthStatus
from app.modules.server_registry.domain.entity.server_check_history import ServerCheckHistory


@pytest.fixture
def mock_server_repository() -> AsyncMock:
    """Mock ServerRepositoryInterface with AsyncMock for async methods"""
    return AsyncMock(spec=ServerRepositoryInterface)


@pytest.fixture
def mock_server_metrics_service() -> AsyncMock:
    """Mock ServerMetricsService - using AsyncMock without spec to avoid import issues"""
    return AsyncMock()


@pytest.fixture
def mock_docker_repository() -> AsyncMock:
    """Mock DockerRepositoryInterface with AsyncMock for async methods"""
    return AsyncMock(spec=DockerRepositoryInterface)


@pytest.fixture
def mock_docker_metrics_service() -> AsyncMock:
    """Mock DockerMetricService - using AsyncMock without spec to avoid import issues"""
    return AsyncMock()


@pytest.fixture
def sample_server() -> Server:
    """Sample Server entity for testing"""
    return Server(
        id=1,
        user_name="testuser",
        ssh_password_encrypted="encrypted_password",
        ip_address="192.168.1.100",
        port=22,
        status=ServerStatus.UP
    )


@pytest.fixture
def sample_server_check_results() -> ServerCheckResults:
    """Sample ServerCheckResults entity for testing"""
    return ServerCheckResults(
        id=1,
        server_id=1,
        status=HealthStatus.HEALTHY,
        check_name="cpu_usage",
        value=25.5,
        unit="%",
        uptime=432000.0,
        checked_at=datetime(2025, 12, 26, 12, 0, 0, tzinfo=timezone.utc)
    )


@pytest.fixture
def sample_server_check_history() -> ServerCheckHistory:
    """Sample ServerCheckHistory entity for testing"""
    return ServerCheckHistory(
        id=1,
        server_id=1,
        status=HealthStatus.HEALTHY,
        check_name="cpu_usage",
        value=25.5,
        unit="%",
        uptime=432000.0,
        checked_at=datetime(2025, 12, 26, 12, 0, 0, tzinfo=timezone.utc)
    )


@pytest.fixture
def sample_server_metrics() -> list[ServerCheckResults]:
    """Sample metrics list returned by ServerMetricsService"""
    return [
        ServerCheckResults(
            server_id=1,
            status=HealthStatus.HEALTHY,
            check_name="cpu_usage",
            value=25.5,
            unit="%",
            uptime=432000.0,
            checked_at=datetime(2025, 12, 26, 12, 0, 0, tzinfo=timezone.utc)
        ),
        ServerCheckResults(
            server_id=1,
            status=HealthStatus.HEALTHY,
            check_name="memory_usage",
            value=60.2,
            unit="%",
            uptime=432000.0,
            checked_at=datetime(2025, 12, 26, 12, 0, 0, tzinfo=timezone.utc)
        )
    ]
