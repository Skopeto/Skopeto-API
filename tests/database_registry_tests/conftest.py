import pytest
from unittest.mock import AsyncMock
from datetime import datetime, timezone

from app.modules.database_registry.domain.repository.database_repository import DatabaseRepositoryInterface
from app.modules.database_registry.domain.entity.database import Database
from app.modules.database_registry.domain.entity.database_health import DatabaseHealth, DatabaseHealthStatus


@pytest.fixture
def mock_database_repository() -> AsyncMock:
    """Mock DatabaseRepositoryInterface with AsyncMock for async methods"""
    return AsyncMock(spec=DatabaseRepositoryInterface)


@pytest.fixture
def mock_database_metrics_service() -> AsyncMock:
    """Mock DatabaseMetricsService - using AsyncMock without spec to avoid import issues"""
    return AsyncMock()


@pytest.fixture
def mock_database_connector() -> AsyncMock:
    """Mock DatabaseConnector - using AsyncMock without spec to avoid import issues"""
    return AsyncMock()


@pytest.fixture
def sample_database() -> Database:
    """Sample Database entity for testing"""
    return Database(
        id=1,
        server_id=1,
        name="test-database",
        db_type="postgresql",
        host="localhost",
        port=5432,
        database_name="testdb",
        service_name=None,
        username="testuser",
        encrypted_password="encrypted_password_hash",
        created_at=datetime(2025, 12, 26, 12, 0, 0, tzinfo=timezone.utc)
    )


@pytest.fixture
def sample_database_health() -> DatabaseHealth:
    """Sample DatabaseHealth entity for testing"""
    return DatabaseHealth(
        id=1,
        database_id=1,
        status=DatabaseHealthStatus.HEALTHY,
        connection_time_ms=50.5,
        is_connected=True,
        query_time_ms=25.3,
        error_message=None,
        checked_at=datetime(2025, 12, 26, 12, 0, 0, tzinfo=timezone.utc)
    )
