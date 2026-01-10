import pytest
from unittest.mock import AsyncMock, patch
from datetime import datetime, timezone

from app.modules.database_registry.application.use_case.register_database import register_database_use_case
from app.modules.database_registry.application.request.register_database_request import RegisterDatabaseRequest
from app.modules.database_registry.domain.entity.database import Database


@pytest.mark.asyncio
async def test_register_database_success(mock_database_repository: AsyncMock):
    """Test successful database registration"""
    # Arrange
    request = RegisterDatabaseRequest(
        server_id=1,
        name="test-database",
        db_type="postgresql",
        host="localhost",
        port=5432,
        database_name="testdb",
        service_name=None,
        username="testuser",
        password="plain_password"
    )

    expected_database = Database(
        id=1,
        server_id=1,
        name="test-database",
        db_type="postgresql",
        host="localhost",
        port=5432,
        database_name="testdb",
        service_name=None,
        username="testuser",
        encrypted_password="encrypted_password_hash",
        created_at=datetime(2025, 12, 26, 12, 0, 0, tzinfo=timezone.utc)
    )

    mock_database_repository.persist_database.return_value = expected_database

    with patch('app.modules.database_registry.application.use_case.register_database.encrypt_password') as mock_encrypt:
        mock_encrypt.return_value = "encrypted_password_hash"

        # Act
        result = await register_database_use_case(
            request=request,
            database_repo=mock_database_repository
        )

    # Assert
    assert result.id == 1
    assert result.server_id == 1
    assert result.name == "test-database"
    assert result.db_type == "postgresql"
    assert result.host == "localhost"
    assert result.port == 5432
    assert result.database_name == "testdb"
    assert result.username == "testuser"
    assert result.encrypted_password == "encrypted_password_hash"
    mock_encrypt.assert_called_once_with("plain_password")
    mock_database_repository.persist_database.assert_called_once()


@pytest.mark.asyncio
async def test_register_database_with_oracle_service_name(mock_database_repository: AsyncMock):
    """Test registering Oracle database with service_name instead of database_name"""
    # Arrange
    request = RegisterDatabaseRequest(
        server_id=1,
        name="oracle-db",
        db_type="oracle",
        host="oracle.example.com",
        port=1521,
        database_name=None,
        service_name="ORCLPDB",
        username="oracleuser",
        password="oracle_password"
    )

    expected_database = Database(
        id=2,
        server_id=1,
        name="oracle-db",
        db_type="oracle",
        host="oracle.example.com",
        port=1521,
        database_name=None,
        service_name="ORCLPDB",
        username="oracleuser",
        encrypted_password="encrypted_oracle_password",
        created_at=datetime(2025, 12, 26, 12, 0, 0, tzinfo=timezone.utc)
    )

    mock_database_repository.persist_database.return_value = expected_database

    with patch('app.modules.database_registry.application.use_case.register_database.encrypt_password') as mock_encrypt:
        mock_encrypt.return_value = "encrypted_oracle_password"

        # Act
        result = await register_database_use_case(
            request=request,
            database_repo=mock_database_repository
        )

    # Assert
    assert result.id == 2
    assert result.db_type == "oracle"
    assert result.service_name == "ORCLPDB"
    assert result.database_name is None
    assert result.encrypted_password == "encrypted_oracle_password"
    mock_encrypt.assert_called_once_with("oracle_password")
    mock_database_repository.persist_database.assert_called_once()


@pytest.mark.asyncio
async def test_register_database_password_encryption(mock_database_repository: AsyncMock):
    """Test that password is properly encrypted and not stored in plain text"""
    # Arrange
    request = RegisterDatabaseRequest(
        server_id=1,
        name="secure-database",
        db_type="mysql",
        host="mysql.example.com",
        port=3306,
        database_name="securedb",
        service_name=None,
        username="secureuser",
        password="MySuperSecretPassword123!"
    )

    with patch('app.modules.database_registry.application.use_case.register_database.encrypt_password') as mock_encrypt:
        mock_encrypt.return_value = "very_encrypted_hash_string"

        def persist_side_effect(database: Database) -> Database:
            database.id = 3
            return database

        mock_database_repository.persist_database.side_effect = persist_side_effect

        # Act
        result = await register_database_use_case(
            request=request,
            database_repo=mock_database_repository
        )

    # Assert
    assert result.encrypted_password == "very_encrypted_hash_string"
    assert result.encrypted_password != "MySuperSecretPassword123!"
    mock_encrypt.assert_called_once_with("MySuperSecretPassword123!")

    # Verify the database entity passed to persist_database has encrypted password
    call_args = mock_database_repository.persist_database.call_args
    persisted_database = call_args[0][0]
    assert persisted_database.encrypted_password == "very_encrypted_hash_string"
