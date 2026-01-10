import pytest
from unittest.mock import AsyncMock, patch
from datetime import datetime, timezone

from app.modules.database_registry.application.use_case.edit_database import edit_database_use_case
from app.modules.database_registry.application.request.update_database_request import UpdateDatabaseRequest
from app.modules.database_registry.domain.entity.database import Database


@pytest.mark.asyncio
async def test_edit_database_success_all_fields(mock_database_repository: AsyncMock, sample_database: Database):
    """Test successful database edit with all fields updated"""
    # Arrange
    database_id = 1
    request = UpdateDatabaseRequest(
        name="updated-database",
        db_type="mysql",
        host="new-host.example.com",
        port=3306,
        database_name="updated_db",
        service_name=None,
        username="newuser",
        password="new_password"
    )

    # Mock repository methods
    mock_database_repository.get_database_by_id.return_value = sample_database

    updated_database = Database(
        id=1,
        server_id=1,
        name="updated-database",
        db_type="mysql",
        host="new-host.example.com",
        port=3306,
        database_name="updated_db",
        service_name=None,
        username="newuser",
        encrypted_password="new_encrypted_password",
        created_at=datetime(2025, 12, 26, 12, 0, 0, tzinfo=timezone.utc)
    )
    mock_database_repository.update_database.return_value = updated_database

    with patch('app.modules.database_registry.application.use_case.edit_database.encrypt_password') as mock_encrypt:
        mock_encrypt.return_value = "new_encrypted_password"

        # Act
        result = await edit_database_use_case(
            id=database_id,
            request=request,
            database_repository=mock_database_repository
        )

    # Assert
    assert result.name == "updated-database"
    assert result.db_type == "mysql"
    assert result.host == "new-host.example.com"
    assert result.port == 3306
    assert result.database_name == "updated_db"
    assert result.username == "newuser"
    assert result.encrypted_password == "new_encrypted_password"

    mock_database_repository.get_database_by_id.assert_called_once_with(database_id)
    mock_database_repository.update_database.assert_called_once()
    mock_encrypt.assert_called_once_with("new_password")


@pytest.mark.asyncio
async def test_edit_database_partial_update(mock_database_repository: AsyncMock, sample_database: Database):
    """Test editing database with only some fields updated"""
    # Arrange
    database_id = 1
    request = UpdateDatabaseRequest(
        name="updated-name",
        port=5433,
        password="new_password"
    )

    # Mock repository methods
    mock_database_repository.get_database_by_id.return_value = sample_database

    # Expected database after update
    updated_database = Database(
        id=1,
        server_id=1,
        name="updated-name",
        db_type="postgresql",  # unchanged
        host="localhost",  # unchanged
        port=5433,  # updated
        database_name="testdb",  # unchanged
        service_name=None,  # unchanged
        username="testuser",  # unchanged
        encrypted_password="new_encrypted_password",  # updated
        created_at=datetime(2025, 12, 26, 12, 0, 0, tzinfo=timezone.utc)
    )
    mock_database_repository.update_database.return_value = updated_database

    with patch('app.modules.database_registry.application.use_case.edit_database.encrypt_password') as mock_encrypt:
        mock_encrypt.return_value = "new_encrypted_password"

        # Act
        result = await edit_database_use_case(
            id=database_id,
            request=request,
            database_repository=mock_database_repository
        )

    # Assert
    assert result.name == "updated-name"
    assert result.port == 5433
    assert result.encrypted_password == "new_encrypted_password"
    # Verify unchanged fields
    assert result.db_type == "postgresql"
    assert result.host == "localhost"
    assert result.username == "testuser"

    mock_database_repository.get_database_by_id.assert_called_once_with(database_id)
    mock_database_repository.update_database.assert_called_once()
    mock_encrypt.assert_called_once_with("new_password")


@pytest.mark.asyncio
async def test_edit_database_no_password_change(mock_database_repository: AsyncMock, sample_database: Database):
    """Test editing database without changing password"""
    # Arrange
    database_id = 1
    request = UpdateDatabaseRequest(
        name="updated-name",
        host="new-host.example.com"
    )

    # Mock repository methods
    mock_database_repository.get_database_by_id.return_value = sample_database

    updated_database = Database(
        id=1,
        server_id=1,
        name="updated-name",
        db_type="postgresql",
        host="new-host.example.com",
        port=5432,
        database_name="testdb",
        service_name=None,
        username="testuser",
        encrypted_password="encrypted_password_hash",  # unchanged
        created_at=datetime(2025, 12, 26, 12, 0, 0, tzinfo=timezone.utc)
    )
    mock_database_repository.update_database.return_value = updated_database

    with patch('app.modules.database_registry.application.use_case.edit_database.encrypt_password') as mock_encrypt:
        # Act
        result = await edit_database_use_case(
            id=database_id,
            request=request,
            database_repository=mock_database_repository
        )

    # Assert
    assert result.name == "updated-name"
    assert result.host == "new-host.example.com"
    assert result.encrypted_password == "encrypted_password_hash"

    # Verify encrypt_password was not called since password wasn't updated
    mock_encrypt.assert_not_called()
    mock_database_repository.get_database_by_id.assert_called_once_with(database_id)
    mock_database_repository.update_database.assert_called_once()


@pytest.mark.asyncio
async def test_edit_database_not_found(mock_database_repository: AsyncMock):
    """Test editing a database that doesn't exist"""
    # Arrange
    database_id = 999
    request = UpdateDatabaseRequest(name="updated-name")

    # Mock repository to return None (database not found)
    mock_database_repository.get_database_by_id.return_value = None

    # Act & Assert
    with pytest.raises(Exception) as exc_info:
        await edit_database_use_case(
            id=database_id,
            request=request,
            database_repository=mock_database_repository
        )

    assert "Database with ID 999 not found" in str(exc_info.value)
    mock_database_repository.get_database_by_id.assert_called_once_with(database_id)
    mock_database_repository.update_database.assert_not_called()


@pytest.mark.asyncio
async def test_edit_database_update_oracle_service_name(mock_database_repository: AsyncMock):
    """Test updating Oracle database service_name"""
    # Arrange
    oracle_database = Database(
        id=2,
        server_id=1,
        name="oracle-db",
        db_type="oracle",
        host="oracle.example.com",
        port=1521,
        database_name=None,
        service_name="ORCLPDB",
        username="oracleuser",
        encrypted_password="encrypted_password",
        created_at=datetime(2025, 12, 26, 12, 0, 0, tzinfo=timezone.utc)
    )

    request = UpdateDatabaseRequest(
        service_name="NEWPDB",
        port=1522
    )

    mock_database_repository.get_database_by_id.return_value = oracle_database

    updated_database = Database(
        id=2,
        server_id=1,
        name="oracle-db",
        db_type="oracle",
        host="oracle.example.com",
        port=1522,
        database_name=None,
        service_name="NEWPDB",
        username="oracleuser",
        encrypted_password="encrypted_password",
        created_at=datetime(2025, 12, 26, 12, 0, 0, tzinfo=timezone.utc)
    )
    mock_database_repository.update_database.return_value = updated_database

    # Act
    result = await edit_database_use_case(
        id=2,
        request=request,
        database_repository=mock_database_repository
    )

    # Assert
    assert result.service_name == "NEWPDB"
    assert result.port == 1522
    assert result.database_name is None
    mock_database_repository.get_database_by_id.assert_called_once_with(2)
    mock_database_repository.update_database.assert_called_once()
