import pytest
from unittest.mock import AsyncMock, patch

from app.modules.server_registry.application.use_case.edit_server import edit_server_use_case
from app.modules.server_registry.application.request.update_server_request import UpdateServerRequest
from app.modules.server_registry.domain.entity.server import Server
from app.modules.server_registry.domain.entity.server_status import ServerStatus
from app.core.Exception import ApplicationException


@pytest.mark.asyncio
async def test_edit_server_success_all_fields(mock_server_repository: AsyncMock, sample_server: Server):
    """Test successful server edit with all fields updated"""
    # Arrange
    server_id = 1
    request = UpdateServerRequest(
        name="updated-server",
        password="new_password",
        ip_address="192.168.1.200",
        port=2222,
        status="up"
    )

    # Mock repository methods
    mock_server_repository.get_server.return_value = sample_server

    updated_server = Server(
        id=1,
        user_name="updated-server",
        ssh_password_encrypted="new_encrypted_password",
        ip_address="192.168.1.200",
        port=2222,
        status=ServerStatus.UP
    )
    mock_server_repository.update_server.return_value = updated_server

    with patch('app.modules.server_registry.application.use_case.edit_server.encrypt_password') as mock_encrypt:
        mock_encrypt.return_value = "new_encrypted_password"

        # Act
        result = await edit_server_use_case(
            server_id=server_id,
            request=request,
            server_repository=mock_server_repository
        )

    # Assert
    assert result.user_name == "updated-server"
    assert result.ssh_password_encrypted == "new_encrypted_password"
    assert result.ip_address == "192.168.1.200"
    assert result.port == 2222
    assert result.status == ServerStatus.UP

    mock_server_repository.get_server.assert_called_once_with(server_id)
    mock_server_repository.update_server.assert_called_once()
    mock_encrypt.assert_called_once_with("new_password")


@pytest.mark.asyncio
async def test_edit_server_partial_update(mock_server_repository: AsyncMock, sample_server: Server):
    """Test editing server with only some fields updated"""
    # Arrange
    server_id = 1
    request = UpdateServerRequest(
        name="new-name",
        port=2222
    )

    # Mock repository methods
    mock_server_repository.get_server.return_value = sample_server

    # Expected server after update
    updated_server = Server(
        id=1,
        user_name="new-name",
        ssh_password_encrypted="encrypted_password",  # unchanged
        ip_address="192.168.1.100",  # unchanged
        port=2222,  # updated
        status=ServerStatus.UP  # unchanged
    )
    mock_server_repository.update_server.return_value = updated_server

    with patch('app.modules.server_registry.application.use_case.edit_server.encrypt_password') as mock_encrypt:
        # Act
        result = await edit_server_use_case(
            server_id=server_id,
            request=request,
            server_repository=mock_server_repository
        )

    # Assert
    assert result.user_name == "new-name"
    assert result.port == 2222
    # Verify unchanged fields
    assert result.ip_address == "192.168.1.100"
    assert result.status == ServerStatus.UP

    mock_server_repository.get_server.assert_called_once_with(server_id)
    mock_server_repository.update_server.assert_called_once()
    # Verify encrypt_password was not called since password wasn't updated
    mock_encrypt.assert_not_called()


@pytest.mark.asyncio
async def test_edit_server_no_password_change(mock_server_repository: AsyncMock, sample_server: Server):
    """Test editing server without changing password"""
    # Arrange
    server_id = 1
    request = UpdateServerRequest(
        name="updated-name",
        ip_address="10.0.0.100"
    )

    # Mock repository methods
    mock_server_repository.get_server.return_value = sample_server

    updated_server = Server(
        id=1,
        user_name="updated-name",
        ssh_password_encrypted="encrypted_password",  # unchanged
        ip_address="10.0.0.100",
        port=22,
        status=ServerStatus.UP
    )
    mock_server_repository.update_server.return_value = updated_server

    with patch('app.modules.server_registry.application.use_case.edit_server.encrypt_password') as mock_encrypt:
        # Act
        result = await edit_server_use_case(
            server_id=server_id,
            request=request,
            server_repository=mock_server_repository
        )

    # Assert
    assert result.user_name == "updated-name"
    assert result.ip_address == "10.0.0.100"
    assert result.ssh_password_encrypted == "encrypted_password"

    # Verify encrypt_password was not called since password wasn't updated
    mock_encrypt.assert_not_called()
    mock_server_repository.get_server.assert_called_once_with(server_id)
    mock_server_repository.update_server.assert_called_once()


@pytest.mark.asyncio
async def test_edit_server_not_found(mock_server_repository: AsyncMock):
    """Test editing a server that doesn't exist"""
    # Arrange
    server_id = 999
    request = UpdateServerRequest(name="updated-name")

    # Mock repository to return None (server not found)
    mock_server_repository.get_server.return_value = None

    # Act & Assert
    with pytest.raises(ApplicationException) as exc_info:
        await edit_server_use_case(
            server_id=server_id,
            request=request,
            server_repository=mock_server_repository
        )

    assert "Server 999 not found" in str(exc_info.value)
    mock_server_repository.get_server.assert_called_once_with(server_id)
    mock_server_repository.update_server.assert_not_called()


@pytest.mark.asyncio
async def test_edit_server_update_status(mock_server_repository: AsyncMock, sample_server: Server):
    """Test updating server status"""
    # Arrange
    server_id = 1
    request = UpdateServerRequest(status="down")

    mock_server_repository.get_server.return_value = sample_server

    updated_server = Server(
        id=1,
        user_name="testuser",
        ssh_password_encrypted="encrypted_password",
        ip_address="192.168.1.100",
        port=22,
        status=ServerStatus.DOWN
    )
    mock_server_repository.update_server.return_value = updated_server

    # Act
    result = await edit_server_use_case(
        server_id=server_id,
        request=request,
        server_repository=mock_server_repository
    )

    # Assert
    assert result.status == ServerStatus.DOWN
    mock_server_repository.get_server.assert_called_once_with(server_id)
    mock_server_repository.update_server.assert_called_once()


@pytest.mark.asyncio
async def test_edit_server_update_to_decommissioned(mock_server_repository: AsyncMock, sample_server: Server):
    """Test updating server status to decommissioned"""
    # Arrange
    server_id = 1
    request = UpdateServerRequest(status="decommissioned")

    mock_server_repository.get_server.return_value = sample_server

    updated_server = Server(
        id=1,
        user_name="testuser",
        ssh_password_encrypted="encrypted_password",
        ip_address="192.168.1.100",
        port=22,
        status=ServerStatus.DECOMISSIONED
    )
    mock_server_repository.update_server.return_value = updated_server

    # Act
    result = await edit_server_use_case(
        server_id=server_id,
        request=request,
        server_repository=mock_server_repository
    )

    # Assert
    assert result.status == ServerStatus.DECOMISSIONED
    mock_server_repository.get_server.assert_called_once_with(server_id)
    mock_server_repository.update_server.assert_called_once()


@pytest.mark.asyncio
async def test_edit_server_password_encryption(mock_server_repository: AsyncMock, sample_server: Server):
    """Test that new password is properly encrypted"""
    # Arrange
    server_id = 1
    request = UpdateServerRequest(password="NewSecurePassword123!")

    mock_server_repository.get_server.return_value = sample_server

    updated_server = Server(
        id=1,
        user_name="testuser",
        ssh_password_encrypted="super_encrypted_new_password",
        ip_address="192.168.1.100",
        port=22,
        status=ServerStatus.UP
    )
    mock_server_repository.update_server.return_value = updated_server

    with patch('app.modules.server_registry.application.use_case.edit_server.encrypt_password') as mock_encrypt:
        mock_encrypt.return_value = "super_encrypted_new_password"

        # Act
        result = await edit_server_use_case(
            server_id=server_id,
            request=request,
            server_repository=mock_server_repository
        )

    # Assert
    assert result.ssh_password_encrypted == "super_encrypted_new_password"
    assert result.ssh_password_encrypted != "NewSecurePassword123!"
    mock_encrypt.assert_called_once_with("NewSecurePassword123!")

    # Verify the server entity passed to update_server has encrypted password
    call_args = mock_server_repository.update_server.call_args
    updated_server_arg = call_args[0][0]
    assert updated_server_arg.ssh_password_encrypted == "super_encrypted_new_password"


@pytest.mark.asyncio
async def test_edit_server_change_ip_and_port(mock_server_repository: AsyncMock, sample_server: Server):
    """Test changing both IP address and port"""
    # Arrange
    server_id = 1
    request = UpdateServerRequest(
        ip_address="10.10.10.10",
        port=2222
    )

    mock_server_repository.get_server.return_value = sample_server

    updated_server = Server(
        id=1,
        user_name="testuser",
        ssh_password_encrypted="encrypted_password",
        ip_address="10.10.10.10",
        port=2222,
        status=ServerStatus.UP
    )
    mock_server_repository.update_server.return_value = updated_server

    # Act
    result = await edit_server_use_case(
        server_id=server_id,
        request=request,
        server_repository=mock_server_repository
    )

    # Assert
    assert result.ip_address == "10.10.10.10"
    assert result.port == 2222
    assert result.user_name == "testuser"  # unchanged
    mock_server_repository.get_server.assert_called_once_with(server_id)
    mock_server_repository.update_server.assert_called_once()
