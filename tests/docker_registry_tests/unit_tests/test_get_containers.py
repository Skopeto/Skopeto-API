import pytest
from unittest.mock import AsyncMock
from datetime import datetime, timezone

from app.modules.docker_registry.application.use_case.get_containers import get_containers_use_case
from app.modules.docker_registry.domain.entity.docker_container import DockerContainer
from app.modules.docker_registry.domain.entity.docker_status import ContainerStatus


@pytest.mark.asyncio
async def test_get_containers_success(
    mock_docker_repository: AsyncMock,
    sample_docker_container: DockerContainer
):
    server_id = 1
    container2 = DockerContainer(
        id=2,
        server_id=server_id,
        container_id="xyz789",
        name="database",
        image="postgres:16",
        status=ContainerStatus.RUNNING,
        ports="5432:5432",
        last_seen_at=datetime(2025, 12, 26, 12, 0, 0, tzinfo=timezone.utc),
        created_at=datetime(2025, 12, 20, 10, 0, 0, tzinfo=timezone.utc),
        updated_at=datetime(2025, 12, 26, 12, 0, 0, tzinfo=timezone.utc)
    )
    mock_docker_repository.get_docker_containers.return_value = [sample_docker_container, container2]

    result = await get_containers_use_case(
        server_id=server_id,
        docker_repository=mock_docker_repository
    )

    assert len(result) == 2
    assert result[0].id == 1
    assert result[0].name == "web-app"
    assert result[0].status == ContainerStatus.RUNNING
    assert result[1].id == 2
    assert result[1].name == "database"
    mock_docker_repository.get_docker_containers.assert_called_once_with(server_id)


@pytest.mark.asyncio
async def test_get_containers_empty_list(
    mock_docker_repository: AsyncMock
):
    server_id = 1
    mock_docker_repository.get_docker_containers.return_value = []

    result = await get_containers_use_case(
        server_id=server_id,
        docker_repository=mock_docker_repository
    )

    assert result == []
    assert len(result) == 0
    mock_docker_repository.get_docker_containers.assert_called_once_with(server_id)


@pytest.mark.asyncio
async def test_get_containers_multiple_statuses(
    mock_docker_repository: AsyncMock
):
    server_id = 1
    containers = [
        DockerContainer(
            id=1,
            server_id=server_id,
            container_id="abc123",
            name="web-app",
            image="nginx:latest",
            status=ContainerStatus.RUNNING,
            ports="80:80",
            last_seen_at=datetime.now(timezone.utc),
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc)
        ),
        DockerContainer(
            id=2,
            server_id=server_id,
            container_id="def456",
            name="old-service",
            image="app:old",
            status=ContainerStatus.EXITED,
            ports="",
            exit_code=0,
            last_seen_at=datetime.now(timezone.utc),
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc)
        ),
        DockerContainer(
            id=3,
            server_id=server_id,
            container_id="ghi789",
            name="paused-app",
            image="app:latest",
            status=ContainerStatus.PAUSED,
            ports="8080:8080",
            last_seen_at=datetime.now(timezone.utc),
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc)
        )
    ]
    mock_docker_repository.get_docker_containers.return_value = containers

    result = await get_containers_use_case(
        server_id=server_id,
        docker_repository=mock_docker_repository
    )

    assert len(result) == 3
    assert result[0].status == ContainerStatus.RUNNING
    assert result[1].status == ContainerStatus.EXITED
    assert result[2].status == ContainerStatus.PAUSED
    mock_docker_repository.get_docker_containers.assert_called_once_with(server_id)


@pytest.mark.asyncio
async def test_get_containers_server_without_containers(
    mock_docker_repository: AsyncMock
):
    server_id = 999
    mock_docker_repository.get_docker_containers.return_value = []

    result = await get_containers_use_case(
        server_id=server_id,
        docker_repository=mock_docker_repository
    )

    assert isinstance(result, list)
    assert len(result) == 0
    mock_docker_repository.get_docker_containers.assert_called_once_with(server_id)
