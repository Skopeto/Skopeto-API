import pytest
from unittest.mock import AsyncMock
from datetime import datetime, timezone

from app.modules.database_registry.application.use_case.delete_database import delete_database_use_case
from app.modules.database_registry.domain.entity.database import Database


@pytest.mark.asyncio
async def test_delete_database_success(mock_database_repository: AsyncMock, sample_database: Database):
    """Test successful database deletion"""
    # Arrange
    database_id = 1
    mock_database_repository.get_database_by_id.return_value = sample_database
    mock_database_repository.delete_database.return_value = None

    # Act
    result = await delete_database_use_case(
        database_id=database_id,
        database_repo=mock_database_repository
    )

    # Assert
    assert result is None
    mock_database_repository.get_database_by_id.assert_called_once_with(database_id)
    mock_database_repository.delete_database.assert_called_once_with(database_id)


@pytest.mark.asyncio
async def test_delete_database_not_found(mock_database_repository: AsyncMock):
    """Test deleting a database that doesn't exist"""
    # Arrange
    database_id = 999
    mock_database_repository.get_database_by_id.return_value = None

    # Act & Assert
    with pytest.raises(ValueError) as exc_info:
        await delete_database_use_case(
            database_id=database_id,
            database_repo=mock_database_repository
        )

    assert "Database not found" in str(exc_info.value)
    mock_database_repository.get_database_by_id.assert_called_once_with(database_id)
    mock_database_repository.delete_database.assert_not_called()


@pytest.mark.asyncio
async def test_delete_database_verify_existence_before_deletion(mock_database_repository: AsyncMock, sample_database: Database):
    """Test that database existence is verified before deletion"""
    # Arrange
    database_id = 1
    mock_database_repository.get_database_by_id.return_value = sample_database
    mock_database_repository.delete_database.return_value = None

    # Act
    await delete_database_use_case(
        database_id=database_id,
        database_repo=mock_database_repository
    )

    # Assert - verify get_database_by_id was called before delete_database
    assert mock_database_repository.get_database_by_id.called
    assert mock_database_repository.delete_database.called

    # Verify call order
    calls = mock_database_repository.method_calls
    get_call = next((i for i, call in enumerate(calls) if 'get_database_by_id' in str(call)), None)
    delete_call = next((i for i, call in enumerate(calls) if 'delete_database' in str(call)), None)

    assert get_call is not None
    assert delete_call is not None
    assert get_call < delete_call, "get_database_by_id should be called before delete_database"


@pytest.mark.asyncio
async def test_delete_database_with_different_ids(mock_database_repository: AsyncMock):
    """Test deletion with various database IDs"""
    # Test with different IDs
    test_ids = [1, 10, 100, 999]

    for db_id in test_ids:
        mock_database_repository.reset_mock()

        # Create a sample database with the test ID
        test_database = Database(
            id=db_id,
            server_id=1,
            name=f"test-database-{db_id}",
            db_type="postgresql",
            host="localhost",
            port=5432,
            database_name="testdb",
            service_name=None,
            username="testuser",
            encrypted_password="encrypted_password",
            created_at=datetime(2025, 12, 26, 12, 0, 0, tzinfo=timezone.utc)
        )

        mock_database_repository.get_database_by_id.return_value = test_database
        mock_database_repository.delete_database.return_value = None

        # Act
        await delete_database_use_case(
            database_id=db_id,
            database_repo=mock_database_repository
        )

        # Assert
        mock_database_repository.get_database_by_id.assert_called_once_with(db_id)
        mock_database_repository.delete_database.assert_called_once_with(db_id)
