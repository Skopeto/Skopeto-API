import pytest
from unittest.mock import AsyncMock, patch
from ipaddress import IPv4Address

from app.modules.server_registry.application.use_case.register_server import register_server_use_case
from app.modules.server_registry.application.request.register_server_location_request import RegisterServerLocationRequest
from app.modules.server_registry.domain.entity.server import Server
from app.modules.server_registry.domain.entity.server_status import ServerStatus


@pytest.mark.asyncio
async def test_register_server_success(mock_server_repository: AsyncMock):
    """Test successful server registration"""
    # Arrange
    request = RegisterServerLocationRequest(
        registrator_id=1,
        name="prod-server",
        password="secure_password",
        ip_address=IPv4Address("192.168.1.100"),
        port=22,
        status=ServerStatus.INACTIVE
    )

    expected_server = Server(
        id=1,
        user_name="prod-server",
        ssh_password_encrypted="encrypted_password_hash",
        ip_address="192.168.1.100",
        port=22,
        status=ServerStatus.INACTIVE
    )

    mock_server_repository.persist_server.return_value = expected_server

    with patch('app.modules.server_registry.application.use_case.register_server.encrypt_password') as mock_encrypt:
        mock_encrypt.return_value = "encrypted_password_hash"

        # Act
        result = await register_server_use_case(
            request=request,
            server_repository=mock_server_repository
        )

    # Assert
    assert result.id == 1
    assert result.user_name == "prod-server"
    assert result.ssh_password_encrypted == "encrypted_password_hash"
    assert result.ip_address == "192.168.1.100"
    assert result.port == 22
    assert result.status == ServerStatus.INACTIVE
    mock_encrypt.assert_called_once_with("secure_password")
    mock_server_repository.persist_server.assert_called_once()


@pytest.mark.asyncio
async def test_register_server_with_up_status(mock_server_repository: AsyncMock):
    """Test registering server with UP status"""
    # Arrange
    request = RegisterServerLocationRequest(
        registrator_id=1,
        name="active-server",
        password="password123",
        ip_address=IPv4Address("10.0.0.50"),
        port=2222,
        status=ServerStatus.UP
    )

    expected_server = Server(
        id=2,
        user_name="active-server",
        ssh_password_encrypted="encrypted_pwd",
        ip_address="10.0.0.50",
        port=2222,
        status=ServerStatus.UP
    )

    mock_server_repository.persist_server.return_value = expected_server

    with patch('app.modules.server_registry.application.use_case.register_server.encrypt_password') as mock_encrypt:
        mock_encrypt.return_value = "encrypted_pwd"

        # Act
        result = await register_server_use_case(
            request=request,
            server_repository=mock_server_repository
        )

    # Assert
    assert result.status == ServerStatus.UP
    assert result.user_name == "active-server"
    assert result.ip_address == "10.0.0.50"
    assert result.port == 2222
    mock_server_repository.persist_server.assert_called_once()


@pytest.mark.asyncio
async def test_register_server_password_encryption(mock_server_repository: AsyncMock):
    """Test that password is properly encrypted and not stored in plain text"""
    # Arrange
    request = RegisterServerLocationRequest(
        registrator_id=1,
        name="secure-server",
        password="MySuperSecretPassword123!",
        ip_address=IPv4Address("172.16.0.100"),
        port=22,
        status=ServerStatus.INACTIVE
    )

    with patch('app.modules.server_registry.application.use_case.register_server.encrypt_password') as mock_encrypt:
        mock_encrypt.return_value = "very_encrypted_hash_string"

        def persist_side_effect(server: Server) -> Server:
            server.id = 3
            return server

        mock_server_repository.persist_server.side_effect = persist_side_effect

        # Act
        result = await register_server_use_case(
            request=request,
            server_repository=mock_server_repository
        )

    # Assert
    assert result.ssh_password_encrypted == "very_encrypted_hash_string"
    assert result.ssh_password_encrypted != "MySuperSecretPassword123!"
    mock_encrypt.assert_called_once_with("MySuperSecretPassword123!")

    # Verify the server entity passed to persist_server has encrypted password
    call_args = mock_server_repository.persist_server.call_args
    persisted_server = call_args[0][0]
    assert persisted_server.ssh_password_encrypted == "very_encrypted_hash_string"


@pytest.mark.asyncio
async def test_register_server_with_ipv6(mock_server_repository: AsyncMock):
    """Test registering server with IPv6 address"""
    # Arrange
    from ipaddress import IPv6Address

    request = RegisterServerLocationRequest(
        registrator_id=1,
        name="ipv6-server",
        password="password123",
        ip_address=IPv6Address("2001:0db8:85a3:0000:0000:8a2e:0370:7334"),
        port=22,
        status=ServerStatus.INACTIVE
    )

    expected_server = Server(
        id=4,
        user_name="ipv6-server",
        ssh_password_encrypted="encrypted_pwd",
        ip_address="2001:db8:85a3::8a2e:370:7334",
        port=22,
        status=ServerStatus.INACTIVE
    )

    mock_server_repository.persist_server.return_value = expected_server

    with patch('app.modules.server_registry.application.use_case.register_server.encrypt_password') as mock_encrypt:
        mock_encrypt.return_value = "encrypted_pwd"

        # Act
        result = await register_server_use_case(
            request=request,
            server_repository=mock_server_repository
        )

    # Assert
    assert result.user_name == "ipv6-server"
    assert "2001" in result.ip_address
    mock_server_repository.persist_server.assert_called_once()


@pytest.mark.asyncio
async def test_register_server_default_inactive_status(mock_server_repository: AsyncMock):
    """Test that default status is INACTIVE when not specified"""
    # Arrange
    request = RegisterServerLocationRequest(
        registrator_id=1,
        name="default-server",
        password="password",
        ip_address=IPv4Address("192.168.1.200"),
        port=22
    )

    expected_server = Server(
        id=5,
        user_name="default-server",
        ssh_password_encrypted="encrypted",
        ip_address="192.168.1.200",
        port=22,
        status=ServerStatus.INACTIVE
    )

    mock_server_repository.persist_server.return_value = expected_server

    with patch('app.modules.server_registry.application.use_case.register_server.encrypt_password') as mock_encrypt:
        mock_encrypt.return_value = "encrypted"

        # Act
        result = await register_server_use_case(
            request=request,
            server_repository=mock_server_repository
        )

    # Assert
    assert result.status == ServerStatus.INACTIVE
    mock_server_repository.persist_server.assert_called_once()


@pytest.mark.asyncio
async def test_register_server_custom_port(mock_server_repository: AsyncMock):
    """Test registering server with custom SSH port"""
    # Arrange
    request = RegisterServerLocationRequest(
        registrator_id=1,
        name="custom-port-server",
        password="password",
        ip_address=IPv4Address("192.168.1.50"),
        port=2222,
        status=ServerStatus.INACTIVE
    )

    expected_server = Server(
        id=6,
        user_name="custom-port-server",
        ssh_password_encrypted="encrypted",
        ip_address="192.168.1.50",
        port=2222,
        status=ServerStatus.INACTIVE
    )

    mock_server_repository.persist_server.return_value = expected_server

    with patch('app.modules.server_registry.application.use_case.register_server.encrypt_password') as mock_encrypt:
        mock_encrypt.return_value = "encrypted"

        # Act
        result = await register_server_use_case(
            request=request,
            server_repository=mock_server_repository
        )

    # Assert
    assert result.port == 2222
    assert result.user_name == "custom-port-server"
    mock_server_repository.persist_server.assert_called_once()
