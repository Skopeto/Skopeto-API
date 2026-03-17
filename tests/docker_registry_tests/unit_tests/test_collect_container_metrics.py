import pytest
from unittest.mock import AsyncMock
from datetime import datetime, timezone

from app.modules.docker_registry.application.use_case.collect_container_metrics import collect_container_metrics_use_case
from app.modules.docker_registry.domain.entity.docker_container import DockerContainer
from app.modules.docker_registry.domain.entity.docker_status import ContainerStatus
from app.modules.server_registry.domain.entity.server import Server
from app.modules.server_registry.domain.entity.server_check_results import ServerHealth, HealthStatus


@pytest.mark.asyncio
async def test_collect_container_metrics_success_new_containers(
    mock_docker_repository: AsyncMock,
    mock_docker_metrics_service: AsyncMock,
    sample_server: Server
):
    server_id = 1
    server_health = ServerHealth(
        server_id=server_id,
        status=HealthStatus.HEALTHY,
        cpu_usage=45.0,
        memory_usage=60.0,
        disk_usage=70.0,
        uptime="10 days",
        checked_at=datetime.now(timezone.utc)
    )

    container_data = [
        {
            'container_id': 'abc123',
            'name': 'web-app',
            'status': ContainerStatus.RUNNING,
            'image': 'nginx:latest',
            'ports': '80:80',
            'server_id': server_id,
            'exit_code': None,
            'is_healthy': True,
            'state_changed_at': None
        },
        {
            'container_id': 'def456',
            'name': 'database',
            'status': ContainerStatus.RUNNING,
            'image': 'postgres:16',
            'ports': '5432:5432',
            'server_id': server_id,
            'exit_code': None,
            'is_healthy': True,
            'state_changed_at': None
        }
    ]

    mock_docker_metrics_service.get_docker_metrics.return_value = container_data
    mock_docker_repository.get_docker_container.return_value = None

    persisted_container = DockerContainer(
        id=1,
        server_id=server_id,
        container_id='abc123',
        name='web-app',
        status=ContainerStatus.RUNNING,
        image='nginx:latest',
        ports='80:80',
        last_seen_at=datetime.now(timezone.utc),
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc)
    )
    mock_docker_repository.persist_docker_container.return_value = persisted_container

    result = await collect_container_metrics_use_case(
        server_id=server_id,
        server=sample_server,
        server_health=server_health,
        docker_repository=mock_docker_repository,
        docker_metrics_service=mock_docker_metrics_service
    )

    assert len(result) == 2
    assert mock_docker_metrics_service.get_docker_metrics.call_count == 1
    assert mock_docker_repository.persist_docker_container.call_count == 2
    assert mock_docker_repository.update_docker_container.call_count == 0


@pytest.mark.asyncio
async def test_collect_container_metrics_updates_existing_containers(
    mock_docker_repository: AsyncMock,
    mock_docker_metrics_service: AsyncMock,
    sample_server: Server,
    sample_docker_container: DockerContainer
):
    server_id = 1
    server_health = ServerHealth(
        server_id=server_id,
        status=HealthStatus.HEALTHY,
        cpu_usage=45.0,
        memory_usage=60.0,
        disk_usage=70.0,
        uptime="10 days",
        checked_at=datetime.now(timezone.utc)
    )

    container_data = [
        {
            'container_id': 'abc123def456',
            'name': 'web-app',
            'status': ContainerStatus.RUNNING,
            'image': 'nginx:latest',
            'ports': '80:80',
            'server_id': server_id,
            'exit_code': None,
            'is_healthy': True,
            'state_changed_at': None
        }
    ]

    mock_docker_metrics_service.get_docker_metrics.return_value = container_data
    mock_docker_repository.get_docker_container.return_value = sample_docker_container

    updated_container = DockerContainer(
        id=1,
        server_id=server_id,
        container_id='abc123def456',
        name='web-app',
        status=ContainerStatus.RUNNING,
        image='nginx:latest',
        ports='80:80',
        last_seen_at=datetime.now(timezone.utc),
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc)
    )
    mock_docker_repository.update_docker_container.return_value = updated_container

    result = await collect_container_metrics_use_case(
        server_id=server_id,
        server=sample_server,
        server_health=server_health,
        docker_repository=mock_docker_repository,
        docker_metrics_service=mock_docker_metrics_service
    )

    assert len(result) == 1
    assert mock_docker_repository.update_docker_container.call_count == 1
    assert mock_docker_repository.persist_docker_container.call_count == 0


@pytest.mark.asyncio
async def test_collect_container_metrics_status_changed(
    mock_docker_repository: AsyncMock,
    mock_docker_metrics_service: AsyncMock,
    sample_server: Server
):
    server_id = 1
    server_health = ServerHealth(
        server_id=server_id,
        status=HealthStatus.HEALTHY,
        cpu_usage=45.0,
        memory_usage=60.0,
        disk_usage=70.0,
        uptime="10 days",
        checked_at=datetime.now(timezone.utc)
    )

    existing_container = DockerContainer(
        id=1,
        server_id=server_id,
        container_id='abc123',
        name='web-app',
        status=ContainerStatus.RUNNING,
        image='nginx:latest',
        ports='80:80',
        last_seen_at=datetime.now(timezone.utc),
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc)
    )

    container_data = [
        {
            'container_id': 'abc123',
            'name': 'web-app',
            'status': ContainerStatus.EXITED,
            'image': 'nginx:latest',
            'ports': '80:80',
            'server_id': server_id,
            'exit_code': 0,
            'is_healthy': False,
            'state_changed_at': None
        }
    ]

    mock_docker_metrics_service.get_docker_metrics.return_value = container_data
    mock_docker_repository.get_docker_container.return_value = existing_container
    mock_docker_repository.update_docker_container.return_value = existing_container

    result = await collect_container_metrics_use_case(
        server_id=server_id,
        server=sample_server,
        server_health=server_health,
        docker_repository=mock_docker_repository,
        docker_metrics_service=mock_docker_metrics_service
    )

    assert len(result) == 1
    mock_docker_repository.update_docker_container.assert_called_once()
    call_args = mock_docker_repository.update_docker_container.call_args[0][0]
    assert call_args.state_changed_at is not None


@pytest.mark.asyncio
async def test_collect_container_metrics_server_unhealthy(
    mock_docker_repository: AsyncMock,
    mock_docker_metrics_service: AsyncMock,
    sample_server: Server
):
    server_id = 1
    server_health = ServerHealth(
        server_id=server_id,
        status=HealthStatus.OFFLINE,
        checked_at=datetime.now(timezone.utc)
    )

    result = await collect_container_metrics_use_case(
        server_id=server_id,
        server=sample_server,
        server_health=server_health,
        docker_repository=mock_docker_repository,
        docker_metrics_service=mock_docker_metrics_service
    )

    assert result == []
    assert len(result) == 0
    mock_docker_metrics_service.get_docker_metrics.assert_not_called()
    mock_docker_repository.persist_docker_container.assert_not_called()


@pytest.mark.asyncio
async def test_collect_container_metrics_server_error(
    mock_docker_repository: AsyncMock,
    mock_docker_metrics_service: AsyncMock,
    sample_server: Server
):
    server_id = 1
    server_health = ServerHealth(
        server_id=server_id,
        status=HealthStatus.ERROR,
        checked_at=datetime.now(timezone.utc)
    )

    result = await collect_container_metrics_use_case(
        server_id=server_id,
        server=sample_server,
        server_health=server_health,
        docker_repository=mock_docker_repository,
        docker_metrics_service=mock_docker_metrics_service
    )

    assert result == []
    mock_docker_metrics_service.get_docker_metrics.assert_not_called()


@pytest.mark.asyncio
async def test_collect_container_metrics_exception_handling(
    mock_docker_repository: AsyncMock,
    mock_docker_metrics_service: AsyncMock,
    sample_server: Server
):
    server_id = 1
    server_health = ServerHealth(
        server_id=server_id,
        status=HealthStatus.HEALTHY,
        cpu_usage=45.0,
        memory_usage=60.0,
        disk_usage=70.0,
        uptime="10 days",
        checked_at=datetime.now(timezone.utc)
    )

    mock_docker_metrics_service.get_docker_metrics.side_effect = Exception("Docker connection failed")

    result = await collect_container_metrics_use_case(
        server_id=server_id,
        server=sample_server,
        server_health=server_health,
        docker_repository=mock_docker_repository,
        docker_metrics_service=mock_docker_metrics_service
    )

    assert result == []
    assert len(result) == 0
    mock_docker_repository.persist_docker_container.assert_not_called()


@pytest.mark.asyncio
async def test_collect_container_metrics_empty_docker_data(
    mock_docker_repository: AsyncMock,
    mock_docker_metrics_service: AsyncMock,
    sample_server: Server
):
    server_id = 1
    server_health = ServerHealth(
        server_id=server_id,
        status=HealthStatus.HEALTHY,
        cpu_usage=45.0,
        memory_usage=60.0,
        disk_usage=70.0,
        uptime="10 days",
        checked_at=datetime.now(timezone.utc)
    )

    mock_docker_metrics_service.get_docker_metrics.return_value = []

    result = await collect_container_metrics_use_case(
        server_id=server_id,
        server=sample_server,
        server_health=server_health,
        docker_repository=mock_docker_repository,
        docker_metrics_service=mock_docker_metrics_service
    )

    assert result == []
    assert len(result) == 0
    mock_docker_repository.persist_docker_container.assert_not_called()
