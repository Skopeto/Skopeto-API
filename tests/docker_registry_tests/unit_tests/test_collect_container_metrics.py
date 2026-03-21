import pytest
from unittest.mock import AsyncMock
from datetime import datetime, timezone

from app.modules.docker_registry.application.use_case.collect_container_metrics import collect_container_metrics_use_case
from app.modules.docker_registry.domain.entity.docker_container import DockerContainer
from app.modules.docker_registry.domain.entity.docker_status import ContainerStatus
from app.modules.server_registry.domain.entity.server import Server
from app.modules.server_registry.domain.entity.server_check_results import ServerCheckResults, HealthStatus


@pytest.mark.asyncio
async def test_collect_container_metrics_success(
    mock_docker_repository: AsyncMock,
    mock_docker_metrics_service: AsyncMock,
    sample_server: Server
):
    server_check_results = [
        ServerCheckResults(
            check_name="cpu",
            value=45.0,
            unit="%",
            status=HealthStatus.HEALTHY,
            server_id=1,
            uptime=45.0,
            checked_at=datetime.now(timezone.utc)
        )
    ]

    container_data = [
        {
            'container_id': 'abc123',
            'name': 'web-app',
            'status': ContainerStatus.RUNNING,
            'image': 'nginx:latest',
            'ports': '80:80',
            'server_id': 1,
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
            'server_id': 1,
            'exit_code': None,
            'is_healthy': True,
            'state_changed_at': None
        }
    ]

    persisted_containers = [
        DockerContainer(
            id=1,
            server_id=1,
            container_id='abc123',
            name='web-app',
            status=ContainerStatus.RUNNING,
            image='nginx:latest',
            ports='80:80',
            last_seen_at=datetime.now(timezone.utc),
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc)
        ),
        DockerContainer(
            id=2,
            server_id=1,
            container_id='def456',
            name='database',
            status=ContainerStatus.RUNNING,
            image='postgres:16',
            ports='5432:5432',
            last_seen_at=datetime.now(timezone.utc),
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc)
        )
    ]

    mock_docker_metrics_service.get_docker_metrics.return_value = container_data
    mock_docker_repository.upsert_docker_containers.return_value = persisted_containers

    result = await collect_container_metrics_use_case(
        server=sample_server,
        server_check_results=server_check_results,
        docker_repository=mock_docker_repository,
        docker_metrics_service=mock_docker_metrics_service
    )

    assert len(result) == 2
    mock_docker_metrics_service.get_docker_metrics.assert_called_once_with(sample_server)
    mock_docker_repository.upsert_docker_containers.assert_called_once()


@pytest.mark.asyncio
async def test_collect_container_metrics_server_offline(
    mock_docker_repository: AsyncMock,
    mock_docker_metrics_service: AsyncMock,
    sample_server: Server
):
    server_check_results = [
        ServerCheckResults(
            check_name="cpu",
            value=0.0,
            unit="%",
            status=HealthStatus.OFFLINE,
            server_id=1,
            uptime=0.0,
            checked_at=datetime.now(timezone.utc)
        )
    ]

    result = await collect_container_metrics_use_case(
        server=sample_server,
        server_check_results=server_check_results,
        docker_repository=mock_docker_repository,
        docker_metrics_service=mock_docker_metrics_service
    )

    assert result == []
    mock_docker_metrics_service.get_docker_metrics.assert_not_called()
    mock_docker_repository.upsert_docker_containers.assert_not_called()


@pytest.mark.asyncio
async def test_collect_container_metrics_server_error(
    mock_docker_repository: AsyncMock,
    mock_docker_metrics_service: AsyncMock,
    sample_server: Server
):
    server_check_results = [
        ServerCheckResults(
            check_name="cpu",
            value=0.0,
            unit="%",
            status=HealthStatus.ERROR,
            server_id=1,
            uptime=0.0,
            checked_at=datetime.now(timezone.utc)
        )
    ]

    result = await collect_container_metrics_use_case(
        server=sample_server,
        server_check_results=server_check_results,
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
    server_check_results = [
        ServerCheckResults(
            check_name="cpu",
            value=45.0,
            unit="%",
            status=HealthStatus.HEALTHY,
            server_id=1,
            uptime=45.0,
            checked_at=datetime.now(timezone.utc)
        )
    ]

    mock_docker_metrics_service.get_docker_metrics.side_effect = Exception("Docker connection failed")

    result = await collect_container_metrics_use_case(
        server=sample_server,
        server_check_results=server_check_results,
        docker_repository=mock_docker_repository,
        docker_metrics_service=mock_docker_metrics_service
    )

    assert result == []
    mock_docker_repository.upsert_docker_containers.assert_not_called()


@pytest.mark.asyncio
async def test_collect_container_metrics_empty_docker_data(
    mock_docker_repository: AsyncMock,
    mock_docker_metrics_service: AsyncMock,
    sample_server: Server
):
    server_check_results = [
        ServerCheckResults(
            check_name="cpu",
            value=45.0,
            unit="%",
            status=HealthStatus.HEALTHY,
            server_id=1,
            uptime=45.0,
            checked_at=datetime.now(timezone.utc)
        )
    ]

    mock_docker_metrics_service.get_docker_metrics.return_value = []

    result = await collect_container_metrics_use_case(
        server=sample_server,
        server_check_results=server_check_results,
        docker_repository=mock_docker_repository,
        docker_metrics_service=mock_docker_metrics_service
    )

    assert result == []
    mock_docker_repository.upsert_docker_containers.assert_not_called()


@pytest.mark.asyncio
async def test_collect_container_metrics_no_check_results(
    mock_docker_repository: AsyncMock,
    mock_docker_metrics_service: AsyncMock,
    sample_server: Server
):
    result = await collect_container_metrics_use_case(
        server=sample_server,
        server_check_results=[],
        docker_repository=mock_docker_repository,
        docker_metrics_service=mock_docker_metrics_service
    )

    assert result == []
    mock_docker_metrics_service.get_docker_metrics.assert_not_called()
