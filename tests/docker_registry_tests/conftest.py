import pytest
from unittest.mock import AsyncMock
from datetime import datetime, timezone

from app.modules.docker_registry.domain.repository.docker_repository import DockerRepositoryInterface
from app.modules.docker_registry.domain.entity.docker_container import DockerContainer
from app.modules.docker_registry.domain.entity.docker_status import ContainerStatus
from app.modules.server_registry.domain.repository.server_repository import ServerRepositoryInterface


@pytest.fixture
def mock_docker_repository() -> AsyncMock:
    """Mock DockerRepositoryInterface with AsyncMock for async methods"""
    return AsyncMock(spec=DockerRepositoryInterface)

@pytest.fixture
def mock_server_repository() -> AsyncMock:
    """Mock ServerRepositoryInterface with AsyncMock for async methods"""
    return AsyncMock(spec=ServerRepositoryInterface)


@pytest.fixture
def mock_docker_metrics_service() -> AsyncMock:
    """Mock DockerMetricService - using AsyncMock without spec to avoid import issues"""
    return AsyncMock()


@pytest.fixture
def sample_docker_container() -> DockerContainer:
    """Sample DockerContainer entity for testing"""
    return DockerContainer(
        id=1,
        server_id=1,
        container_id="abc123def456",
        name="web-app",
        image="nginx:latest",
        status=ContainerStatus.RUNNING,
        ports="80:80",
        last_seen_at=datetime(2025, 12, 26, 12, 0, 0, tzinfo=timezone.utc),
        created_at=datetime(2025, 12, 20, 10, 0, 0, tzinfo=timezone.utc),
        updated_at=datetime(2025, 12, 26, 12, 0, 0, tzinfo=timezone.utc)
    )


@pytest.fixture
def sample_docker_container_data() -> dict:
    """Sample container data dict returned by DockerMetricService"""
    return {
        'container_id': 'abc123def456',
        'name': 'web-app',
        'status': ContainerStatus.RUNNING,
        'image': 'nginx:latest',
        'ports': '80:80',
        'server_id': 1,
        'exit_code': None,
        'is_healthy': None,
        'state_changed_at': None
    }
