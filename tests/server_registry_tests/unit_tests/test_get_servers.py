import pytest
from unittest.mock import AsyncMock

from app.modules.server_registry.application.use_case.get_servers import get_servers_use_case
from app.modules.server_registry.domain.entity.server import Server, ServerStatus
from app.modules.server_registry.domain.repository.server_repository import ServerRepositoryInterface


@pytest.mark.asyncio
async def test_get_servers_success(mock_server_repository: AsyncMock, sample_server: Server):
    """Test successful retrieval of servers"""
    # Arrange
    server2 = Server(
        id=2,
        user_name="testuser2",
        ssh_password_encrypted="encrypted2",
        ip_address="192.168.1.101",
        port=22,
        status=ServerStatus.UP
    )
    mock_server_repository.get_all_servers.return_value = [sample_server, server2]

    # Act
    result = await get_servers_use_case(server_repository=mock_server_repository)

    # Assert
    assert len(result) == 2
    assert result[0].id == 1
    assert result[0].ip_address == "192.168.1.100"
    assert result[1].id == 2
    assert result[1].ip_address == "192.168.1.101"
    mock_server_repository.get_all_servers.assert_called_once()


@pytest.mark.asyncio
async def test_get_servers_empty_list(mock_server_repository: AsyncMock):
    """Test when no servers exist"""
    # Arrange
    mock_server_repository.get_all_servers.return_value = []

    # Act
    result = await get_servers_use_case(server_repository=mock_server_repository)

    # Assert
    assert result == []
    assert len(result) == 0
    mock_server_repository.get_all_servers.assert_called_once()
