import pytest
from unittest.mock import AsyncMock

from app.core.Exception import ApplicationException, SSHConnectionException
from app.modules.docker_registry.application.use_case.collect_docker_container import collect_docker_container_data_use_case
from app.modules.docker_registry.domain.entity.docker_container import DockerContainer
from app.modules.docker_registry.domain.entity.docker_status import ContainerStatus
from app.modules.server_registry.domain.entity.server import Server, ServerStatus


@pytest.mark.asyncio
async def test_collect_docker_container_success_all_new(
    mock_server_repository: AsyncMock,
    mock_docker_repository: AsyncMock,
    mock_docker_metrics_service: AsyncMock,
    sample_docker_container_data: dict
):
    """Test successful collection when all containers are new"""
    # Arrange
    server = Server(
        id=1,
        user_name="testuser",
        ssh_password_encrypted="encrypted",
        ip_address="192.168.1.100",
        port=22,
        status=ServerStatus.UP
    )

    container_data_2 = {
        'container_id': 'xyz789ghi012',
        'name': 'database',
        'status': ContainerStatus.RUNNING,
        'image': 'postgres:14',
        'ports': '5432:5432',
        'server_id': 1,
        'exit_code': None,
        'is_healthy': None,
        'state_changed_at': None
    }

    mock_server_repository.get_server.return_value = server
    mock_docker_metrics_service.get_docker_metrics.return_value = [
        sample_docker_container_data,
        container_data_2
    ]
    mock_docker_repository.get_docker_container.return_value = None

    def persist_side_effect(container: DockerContainer) -> DockerContainer:
        """Simulate database ID assignment"""
        container.id = 1 if container.container_id == 'abc123def456' else 2
        return container

    mock_docker_repository.persist_docker_container.side_effect = persist_side_effect

    # Act
    result = await collect_docker_container_data_use_case(
        server_id=1,
        docker_service=mock_docker_metrics_service,
        server_repository=mock_server_repository,
        docker_repository=mock_docker_repository
    )

    # Assert
    assert len(result) == 2
    assert result[0].container_id == 'abc123def456'
    assert result[1].container_id == 'xyz789ghi012'
    mock_server_repository.get_server.assert_called_once_with(1)
    mock_docker_metrics_service.get_docker_metrics.assert_called_once_with(server)
    assert mock_docker_repository.persist_docker_container.call_count == 2
    mock_docker_repository.update_docker_container.assert_not_called()


@pytest.mark.asyncio
async def test_collect_docker_container_success_all_existing(
    mock_server_repository: AsyncMock,
    mock_docker_repository: AsyncMock,
    mock_docker_metrics_service: AsyncMock,
    sample_docker_container_data: dict,
    sample_docker_container: DockerContainer
):
    """Test successful collection when all containers already exist"""
    # Arrange
    server = Server(
        id=1,
        user_name="testuser",
        ssh_password_encrypted="encrypted",
        ip_address="192.168.1.100",
        port=22,
        status=ServerStatus.UP
    )

    mock_server_repository.get_server.return_value = server
    mock_docker_metrics_service.get_docker_metrics.return_value = [sample_docker_container_data]
    mock_docker_repository.get_docker_container.return_value = sample_docker_container
    mock_docker_repository.update_docker_container.return_value = sample_docker_container

    # Act
    result = await collect_docker_container_data_use_case(
        server_id=1,
        docker_service=mock_docker_metrics_service,
        server_repository=mock_server_repository,
        docker_repository=mock_docker_repository
    )

    # Assert
    assert len(result) == 1
    assert result[0].container_id == 'abc123def456'
    mock_docker_repository.update_docker_container.assert_called_once()
    mock_docker_repository.persist_docker_container.assert_not_called()


@pytest.mark.asyncio
async def test_collect_docker_container_success_mixed(
    mock_server_repository: AsyncMock,
    mock_docker_repository: AsyncMock,
    mock_docker_metrics_service: AsyncMock,
    sample_docker_container_data: dict,
    sample_docker_container: DockerContainer
):
    """Test successful collection with mix of new and existing containers"""
    # Arrange
    server = Server(
        id=1,
        user_name="testuser",
        ssh_password_encrypted="encrypted",
        ip_address="192.168.1.100",
        port=22,
        status=ServerStatus.UP
    )

    container_data_2 = {
        'container_id': 'xyz789ghi012',
        'name': 'database',
        'status': ContainerStatus.RUNNING,
        'image': 'postgres:14',
        'ports': '5432:5432',
        'server_id': 1,
        'exit_code': None,
        'is_healthy': None,
        'state_changed_at': None
    }

    mock_server_repository.get_server.return_value = server
    mock_docker_metrics_service.get_docker_metrics.return_value = [
        sample_docker_container_data,
        container_data_2
    ]

    # First container exists, second is new
    async def get_docker_container_side_effect(container_id, server_id):
        if container_id == 'abc123def456':
            return sample_docker_container
        return None

    mock_docker_repository.get_docker_container.side_effect = get_docker_container_side_effect
    mock_docker_repository.update_docker_container.return_value = sample_docker_container

    new_container = DockerContainer(**container_data_2)
    new_container.id = 2
    mock_docker_repository.persist_docker_container.return_value = new_container

    # Act
    result = await collect_docker_container_data_use_case(
        server_id=1,
        docker_service=mock_docker_metrics_service,
        server_repository=mock_server_repository,
        docker_repository=mock_docker_repository
    )

    # Assert
    assert len(result) == 2
    mock_docker_repository.update_docker_container.assert_called_once()
    mock_docker_repository.persist_docker_container.assert_called_once()


@pytest.mark.asyncio
async def test_collect_docker_container_server_not_found(
    mock_server_repository: AsyncMock,
    mock_docker_repository: AsyncMock,
    mock_docker_metrics_service: AsyncMock
):
    """Test when server is not found"""
    # Arrange
    mock_server_repository.get_server.return_value = None

    # Act & Assert
    with pytest.raises(ApplicationException, match="Server 1 not found"):
        await collect_docker_container_data_use_case(
            server_id=1,
            docker_service=mock_docker_metrics_service,
            server_repository=mock_server_repository,
            docker_repository=mock_docker_repository
        )

    mock_server_repository.get_server.assert_called_once_with(1)
    mock_docker_metrics_service.get_docker_metrics.assert_not_called()


@pytest.mark.asyncio
async def test_collect_docker_container_no_containers_found(
    mock_server_repository: AsyncMock,
    mock_docker_repository: AsyncMock,
    mock_docker_metrics_service: AsyncMock
):
    """Test when no containers are found on the server"""
    # Arrange
    server = Server(
        id=1,
        user_name="testuser",
        ssh_password_encrypted="encrypted",
        ip_address="192.168.1.100",
        port=22,
        status=ServerStatus.UP
    )

    mock_server_repository.get_server.return_value = server
    mock_docker_metrics_service.get_docker_metrics.return_value = []

    # Act & Assert
    with pytest.raises(ApplicationException, match="No containers found on server 1"):
        await collect_docker_container_data_use_case(
            server_id=1,
            docker_service=mock_docker_metrics_service,
            server_repository=mock_server_repository,
            docker_repository=mock_docker_repository
        )

    mock_docker_metrics_service.get_docker_metrics.assert_called_once()


@pytest.mark.asyncio
async def test_collect_docker_container_ssh_connection_error(
    mock_server_repository: AsyncMock,
    mock_docker_repository: AsyncMock,
    mock_docker_metrics_service: AsyncMock
):
    """Test when SSH connection fails"""
    # Arrange
    server = Server(
        id=1,
        user_name="testuser",
        ssh_password_encrypted="encrypted",
        ip_address="192.168.1.100",
        port=22,
        status=ServerStatus.UP
    )

    mock_server_repository.get_server.return_value = server
    mock_docker_metrics_service.get_docker_metrics.side_effect = SSHConnectionException("Connection timeout")

    # Act & Assert
    with pytest.raises(SSHConnectionException, match="Connection timeout"):
        await collect_docker_container_data_use_case(
            server_id=1,
            docker_service=mock_docker_metrics_service,
            server_repository=mock_server_repository,
            docker_repository=mock_docker_repository
        )

    mock_docker_metrics_service.get_docker_metrics.assert_called_once()
