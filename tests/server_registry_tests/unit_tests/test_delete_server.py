import pytest
from unittest.mock import AsyncMock

from app.modules.server_registry.application.use_case.delete_server import delete_server_use_case


@pytest.mark.asyncio
async def test_delete_server_success(mock_server_repository: AsyncMock):
    """Test successful server deletion"""
    # Arrange
    server_id = 1
    mock_server_repository.delete_server.return_value = None

    # Act
    result = await delete_server_use_case(
        server_id=server_id,
        server_repository=mock_server_repository
    )

    # Assert
    assert result is None
    mock_server_repository.delete_server.assert_called_once_with(server_id)


@pytest.mark.asyncio
async def test_delete_server_with_different_ids(mock_server_repository: AsyncMock):
    """Test deletion with various server IDs"""
    # Test with different IDs
    test_ids = [1, 10, 100, 999]

    for server_id in test_ids:
        mock_server_repository.reset_mock()
        mock_server_repository.delete_server.return_value = None

        # Act
        result = await delete_server_use_case(
            server_id=server_id,
            server_repository=mock_server_repository
        )

        # Assert
        assert result is None
        mock_server_repository.delete_server.assert_called_once_with(server_id)


@pytest.mark.asyncio
async def test_delete_server_repository_called_correctly(mock_server_repository: AsyncMock):
    """Test that repository delete method is called with correct parameter"""
    # Arrange
    server_id = 42
    mock_server_repository.delete_server.return_value = None

    # Act
    await delete_server_use_case(
        server_id=server_id,
        server_repository=mock_server_repository
    )

    # Assert
    # Verify the exact arguments passed to delete_server
    call_args = mock_server_repository.delete_server.call_args
    assert call_args[0][0] == server_id
    mock_server_repository.delete_server.assert_called_once()
