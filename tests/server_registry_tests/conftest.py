import pytest
from unittest.mock import AsyncMock
from datetime import datetime, timezone

from app.modules.server_registry.domain.repository.server_repository import ServerRepositoryInterface
from app.modules.server_registry.domain.entity.server import Server, ServerStatus
from app.modules.server_registry.domain.entity.server_health import ServerHealth, HealthStatus
from app.modules.server_registry.domain.entity.server_history import ServerHistory, HealthStatushistory


@pytest.fixture
def mock_server_repository() -> AsyncMock:
    """Mock ServerRepositoryInterface with AsyncMock for async methods"""
    return AsyncMock(spec=ServerRepositoryInterface)


@pytest.fixture
def mock_server_metrics_service() -> AsyncMock:
    """Mock ServerMetricsService - using AsyncMock without spec to avoid import issues"""
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
def sample_server_health() -> ServerHealth:
    """Sample ServerHealth entity for testing"""
    return ServerHealth(
        id=1,
        server_id=1,
        status=HealthStatus.HEALTHY,
        cpu_usage=25.5,
        memory_usage=60.2,
        disk_usage=45.0,
        uptime="up 5 days",
        checked_at=datetime(2025, 12, 26, 12, 0, 0, tzinfo=timezone.utc)
    )

@pytest.fixture
def sample_server_history() -> ServerHistory:
    """Sample ServerHistory entity for testing"""
    return ServerHistory(
        id=1,
        server_id=1,
        status=HealthStatushistory.HEALTHY,
        cpu_usage=25.5,
        memory_usage=60.2,
        disk_usage=45.0,
        uptime="up 5 days",
        checked_at=datetime(2025, 12, 26, 12, 0, 0, tzinfo=timezone.utc)
    )


@pytest.fixture
def sample_server_metrics() -> dict:
    """Sample metrics dict returned by ServerMetricsService"""
    return {
        'cpu_usage': 25.5,
        'memory_usage': 60.2,
        'disk_usage': 45.0,
        'uptime': 'up 5 days',
        'server_id': 1
    }
