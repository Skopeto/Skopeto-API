import pytest
from unittest.mock import AsyncMock
from datetime import datetime, timezone

from app.modules.database_registry.application.use_case.get_databases import get_databases_use_case
from app.modules.database_registry.domain.entity.database import Database


@pytest.mark.asyncio
async def test_get_databases_success(mock_database_repository: AsyncMock, sample_database: Database):
    """Test successful retrieval of databases for a server"""
    # Arrange
    server_id = 1
    database2 = Database(
        id=2,
        server_id=1,
        name="second-database",
        db_type="mysql",
        host="mysql.example.com",
        port=3306,
        database_name="mysqldb",
        service_name=None,
        username="mysqluser",
        encrypted_password="encrypted_password2",
        created_at=datetime(2025, 12, 26, 13, 0, 0, tzinfo=timezone.utc)
    )

    mock_database_repository.get_databases_by_server_id.return_value = [sample_database, database2]

    # Act
    result = await get_databases_use_case(
        server_id=server_id,
        database_repository=mock_database_repository
    )

    # Assert
    assert len(result) == 2
    assert result[0].id == 1
    assert result[0].name == "test-database"
    assert result[0].db_type == "postgresql"
    assert result[1].id == 2
    assert result[1].name == "second-database"
    assert result[1].db_type == "mysql"
    mock_database_repository.get_databases_by_server_id.assert_called_once_with(server_id)


@pytest.mark.asyncio
async def test_get_databases_empty_list(mock_database_repository: AsyncMock):
    """Test when no databases exist for a server"""
    # Arrange
    server_id = 999
    mock_database_repository.get_databases_by_server_id.return_value = []

    # Act
    result = await get_databases_use_case(
        server_id=server_id,
        database_repository=mock_database_repository
    )

    # Assert
    assert result == []
    assert len(result) == 0
    mock_database_repository.get_databases_by_server_id.assert_called_once_with(server_id)


@pytest.mark.asyncio
async def test_get_databases_multiple_types(mock_database_repository: AsyncMock):
    """Test retrieval of databases with different types"""
    # Arrange
    server_id = 1

    postgres_db = Database(
        id=1,
        server_id=1,
        name="postgres-db",
        db_type="postgresql",
        host="postgres.example.com",
        port=5432,
        database_name="postgresdb",
        service_name=None,
        username="pguser",
        encrypted_password="encrypted1",
        created_at=datetime(2025, 12, 26, 12, 0, 0, tzinfo=timezone.utc)
    )

    mysql_db = Database(
        id=2,
        server_id=1,
        name="mysql-db",
        db_type="mysql",
        host="mysql.example.com",
        port=3306,
        database_name="mysqldb",
        service_name=None,
        username="mysqluser",
        encrypted_password="encrypted2",
        created_at=datetime(2025, 12, 26, 12, 0, 0, tzinfo=timezone.utc)
    )

    oracle_db = Database(
        id=3,
        server_id=1,
        name="oracle-db",
        db_type="oracle",
        host="oracle.example.com",
        port=1521,
        database_name=None,
        service_name="ORCLPDB",
        username="oracleuser",
        encrypted_password="encrypted3",
        created_at=datetime(2025, 12, 26, 12, 0, 0, tzinfo=timezone.utc)
    )

    mock_database_repository.get_databases_by_server_id.return_value = [postgres_db, mysql_db, oracle_db]

    # Act
    result = await get_databases_use_case(
        server_id=server_id,
        database_repository=mock_database_repository
    )

    # Assert
    assert len(result) == 3
    assert result[0].db_type == "postgresql"
    assert result[0].database_name == "postgresdb"
    assert result[1].db_type == "mysql"
    assert result[1].database_name == "mysqldb"
    assert result[2].db_type == "oracle"
    assert result[2].service_name == "ORCLPDB"
    mock_database_repository.get_databases_by_server_id.assert_called_once_with(server_id)


@pytest.mark.asyncio
async def test_get_databases_verify_server_isolation(mock_database_repository: AsyncMock):
    """Test that only databases for the specified server are returned"""
    # Arrange
    server_id = 1

    # Databases for server 1
    db_server1 = Database(
        id=1,
        server_id=1,
        name="db-server1",
        db_type="postgresql",
        host="localhost",
        port=5432,
        database_name="db1",
        service_name=None,
        username="user1",
        encrypted_password="encrypted1",
        created_at=datetime(2025, 12, 26, 12, 0, 0, tzinfo=timezone.utc)
    )

    mock_database_repository.get_databases_by_server_id.return_value = [db_server1]

    # Act
    result = await get_databases_use_case(
        server_id=server_id,
        database_repository=mock_database_repository
    )

    # Assert
    assert len(result) == 1
    assert all(db.server_id == server_id for db in result)
    mock_database_repository.get_databases_by_server_id.assert_called_once_with(server_id)
